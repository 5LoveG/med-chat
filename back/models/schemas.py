from pydantic import BaseModel


class ChatRequest(BaseModel):
    text: str
    session_id: str = None


class ChatResponse(BaseModel):
    response: str
    session_id: str
