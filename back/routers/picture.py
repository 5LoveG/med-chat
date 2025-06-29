from fastapi import HTTPException, File, UploadFile, APIRouter
from fastapi.responses import JSONResponse
from PIL import Image
import io
import easyocr

router = APIRouter()


@router.post("/picture")
async def extract_text(image: UploadFile = File(default=None)):
    # 检查文件是否上传
    if not image:
        raise HTTPException(status_code=400, detail="未上传文件")

    try:
        # 读取图像文件内容
        contents = await image.read()
        img = Image.open(io.BytesIO(contents))

        reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)
        # 路径改为用户需要识别的图片的路径
        text = reader.readtext(img, detail=0)

        if not text:
            return {"text": "未识别到文字"}
        else:
            return {"text": text}

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
