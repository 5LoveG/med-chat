import json
import os
from datetime import datetime
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage, AIMessage
from models.schemas import ChatRequest
from services.llm_service import *
from utils.llm_utils import streaming_chain, get_title, switch_rag, switch_department

router = APIRouter()


@router.post("/rag/{num}")
async def rag(num: int):
    global chain
    chain = switch_rag(num)
    return num


@router.post("/analysis/{text}")
async def analysis(text: str):
    full_response = []
    history_messages = []

    async def generate():
        async for chunk in streaming_chain(text, history_messages, chain2):
            # 发送每个chunk到客户端
            yield chunk
            # 同时收集完整响应
            data = json.loads(chunk.split('data: ')[1])
            full_response.append(data['content'])

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Content-Type": "text/event-stream"}
    )


@router.post("/road/{text}")
async def road(text: str):
    full_response = []
    history_messages = []

    async def generate():
        async for chunk in streaming_chain(text, history_messages, chain3):
            # 发送每个chunk到客户端
            yield chunk
            # 同时收集完整响应
            data = json.loads(chunk.split('data: ')[1])
            full_response.append(data['content'])

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Content-Type": "text/event-stream"}
    )


@router.post("/chooseDepartment/{department}")
async def rag(department: str):
    global chain
    chain = switch_department(department)
    return department


@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    if not request.session_id:
        session_id = session_storage.create_session()
    else:
        session_id = request.session_id

    history_messages = []
    for msg in session_storage.get_history(session_id):
        if msg["role"] == "user":
            history_messages.append(HumanMessage(content=msg["content"]))
        else:
            history_messages.append(AIMessage(content=msg["content"]))

    # 先保存用户消息
    session_storage.add_message(session_id, "user", request.text)

    # 创建临时保存assistant消息的变量
    full_response = []

    async def generate():
        async for chunk in streaming_chain(request.text, history_messages, chain):
            # 发送每个chunk到客户端
            yield chunk
            # 同时收集完整响应
            data = json.loads(chunk.split('data: ')[1])
            full_response.append(data['content'])

        # 最终保存完整响应
        session_storage.add_message(session_id, "assistant", "".join(full_response))

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Content-Type": "text/event-stream"}
    )


@router.get("/new")
async def new_session():
    session_id = session_storage.create_session()
    session = {
        "title": datetime.now().strftime("%m-%d %H:%M"),
        "id": session_id
    }
    return session


@router.delete("/delete/{session_id}")  # 空的不能删
async def delete_session(session_id: str):
    print(session_id)
    session_storage.delete_session(session_id)
    return {"message": "Session deleted successfully"}


@router.get("/history/{session_id}")  # 切换会话时显示所有历史记录
async def get_session_history(session_id: str):
    session_history = {
        "history": session_storage.get_history(session_id),
        "id": session_id
    }
    return session_history


@router.get("/sessions")
async def session_list():
    sessions = []
    for f in os.listdir("Local/Sessions"):
        title = get_title("Local/Sessions/" + f)
        current_time = datetime.now().strftime("%m-%d %H:%M")
        if not title:
            title = current_time
        if f.endswith('.json'):
            file_id = os.path.splitext(f)[0]
            sessions.append({
                "title": title,
                "id": file_id
            })
    return sessions
