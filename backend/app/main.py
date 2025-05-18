from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import os
from .utils import save_upload_file, UPLOAD_FOLDER
from .models import Image
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = FastAPI(title="SnapURL API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, set this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
try:
    MONGODB_URL = os.getenv("MONGODB_URL")
    if not MONGODB_URL:
        raise ValueError("MONGODB_URL environment variable is not set")
    
    client = AsyncIOMotorClient(MONGODB_URL)
    # Test the connection
    client.admin.command('ping')
    logger.info("Successfully connected to MongoDB")
    
    db = client.snapurl
    images = db.images
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {str(e)}")
    raise

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Mount the uploads directory
app.mount("/images", StaticFiles(directory=UPLOAD_FOLDER), name="images")

# API routes with /api prefix
@app.post("/api/upload")
async def upload_image(file: UploadFile = File(...)):
    try:
        file_path, image_url = await save_upload_file(file)
        
        # Create image document
        image_doc = {
            "filename": file.filename,
            "url": image_url,
            "uploaded_at": datetime.utcnow(),
            "size": os.path.getsize(file_path),
            "content_type": file.content_type
        }
        
        # Save to MongoDB
        await images.insert_one(image_doc)
        
        return {"url": image_url, "filename": file.filename}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/images")
async def list_images():
    try:
        cursor = images.find({}, {"_id": 0})
        return await cursor.to_list(length=100)
    except Exception as e:
        logger.error(f"Error fetching images: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    try:
        # Test MongoDB connection
        await client.admin.command('ping')
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow(),
            "mongodb": "connected"
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to SnapURL API. Visit /docs for API documentation."}
