import os
from fastapi import FastAPI, HTTPException, File, UploadFile, BackgroundTasks, APIRouter
from werkzeug.utils import secure_filename
import shutil
from config import MAX_FILE_SIZE, UPLOAD_FOLDER
from services import audio_model
from utils import cleanup_file

router = APIRouter()


@router.post("/audio")
async def upload_audio(
        background_tasks: BackgroundTasks,
        file: UploadFile = File(..., max_size=MAX_FILE_SIZE)
):
    # 检查文件是否存在
    if not file:
        raise HTTPException(status_code=400, detail="未收到文件")

    # 检查文件名是否有效
    if not file.filename or file.filename.strip() == '':
        raise HTTPException(status_code=400, detail="无效文件名")

    try:
        # 生成安全文件名
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        # 保存上传文件
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 语音识别
        result = audio_model.transcribe(file_path, language="zh", fp16=True)
        if not result["text"]:
            result["text"] = "识别失败,请重新说明"
        # 添加后台清理任务
        background_tasks.add_task(cleanup_file, file_path)
        print(result)
        return {
            "message": "文件上传成功",
            "text": result["text"].strip()
        }

    except Exception as e:
        # 异常时清理临时文件
        if 'file_path' in locals() and os.path.exists(file_path):
            cleanup_file(file_path)
        raise HTTPException(
            status_code=500,
            detail=f"处理失败: {str(e)}"
        )
