import os
from fastapi import UploadFile
import shutil
from typing import Tuple

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def ensure_upload_folder():
    """Ensure the upload folder exists"""
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename: str) -> bool:
    """Check if the file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

async def save_upload_file(upload_file: UploadFile) -> Tuple[str, str]:
    """Save the uploaded file and return the file path and URL"""
    ensure_upload_folder()
    
    if not allowed_file(upload_file.filename):
        raise ValueError("File type not allowed")
    
    file_path = os.path.join(UPLOAD_FOLDER, upload_file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    
    # For local development, use localhost
    image_url = f"http://localhost:8000/images/{upload_file.filename}"
    
    return file_path, image_url
