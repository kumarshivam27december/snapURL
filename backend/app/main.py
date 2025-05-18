from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import os
from .utils import save_upload_file, UPLOAD_FOLDER
from .models import Image
from dotenv import load_dotenv
import logging
from bson import ObjectId
import shutil

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

# Get the deployed domain from environment variable or use a default
DEPLOYED_DOMAIN = os.getenv("DEPLOYED_DOMAIN", "https://snapurl-xrth.onrender.com")

# API routes with /api prefix
@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Create a safe filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(UPLOAD_FOLDER, safe_filename)
        
        # Save the file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Create image document
        image_doc = {
            "filename": safe_filename,
            "original_filename": file.filename,
            "url": f"{DEPLOYED_DOMAIN}/images/{safe_filename}",
            "uploaded_at": datetime.utcnow()
        }
        
        # Save to MongoDB
        result = await images.insert_one(image_doc)
        image_doc["_id"] = str(result.inserted_id)
        
        return image_doc
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/images")
async def get_images():
    try:
        images = []
        async for image in images.find().sort("uploaded_at", -1):
            image["_id"] = str(image["_id"])
            images.append(image)
        return images
    except Exception as e:
        logger.error(f"Error fetching images: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/images/{image_id}")
async def delete_image(image_id: str):
    try:
        # Get image details from MongoDB
        image = await images.find_one({"_id": ObjectId(image_id)})
        if not image:
            raise HTTPException(status_code=404, detail="Image not found")
        
        # Delete file from filesystem
        file_path = os.path.join(UPLOAD_FOLDER, image["filename"])
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Delete from MongoDB
        await images.delete_one({"_id": ObjectId(image_id)})
        
        return {"message": "Image deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting image: {e}")
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
