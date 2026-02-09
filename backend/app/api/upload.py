"""
文件上传接口
"""
import os
import uuid
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import FileResponse

from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()

# 上传目录
UPLOAD_DIR = "/app/uploads"
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


def ensure_upload_dir():
    """确保上传目录存在"""
    os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/image")
async def upload_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """上传图片"""
    ensure_upload_dir()
    
    # 检查文件扩展名
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"不支持的文件类型，仅支持: {', '.join(ALLOWED_EXTENSIONS)}")
    
    # 读取文件内容
    content = await file.read()
    
    # 检查文件大小
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="文件大小不能超过 10MB")
    
    # 生成唯一文件名
    date_path = datetime.now().strftime("%Y/%m")
    unique_name = f"{uuid.uuid4().hex}{ext}"
    
    # 创建日期目录
    full_dir = os.path.join(UPLOAD_DIR, date_path)
    os.makedirs(full_dir, exist_ok=True)
    
    # 保存文件
    file_path = os.path.join(full_dir, unique_name)
    with open(file_path, "wb") as f:
        f.write(content)
    
    # 返回访问 URL
    url = f"/api/upload/images/{date_path}/{unique_name}"
    return {"url": url}


@router.get("/images/{year}/{month}/{filename}")
async def get_image(year: str, month: str, filename: str):
    """获取上传的图片"""
    file_path = os.path.join(UPLOAD_DIR, year, month, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="图片不存在")
    
    return FileResponse(file_path)
