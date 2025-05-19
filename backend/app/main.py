from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import os
from .utils import UPLOAD_FOLDER
from dotenv import load_dotenv
import logging
from bson import ObjectId
import shutil

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load .env only for MONGODB_URL
load_dotenv()

app = FastAPI(title="SnapURL API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
MONGODB_URL = os.getenv("MONGODB_URL")
if not MONGODB_URL:
    raise ValueError("MONGODB_URL environment variable is not set")

try:
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client.snapurl
    images = db.images
    logger.info("Successfully connected to MongoDB")
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {e}")
    raise

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.mount("/images", StaticFiles(directory=UPLOAD_FOLDER), name="images")

# Hard‑coded public URL of your Render deployment
BASE_URL = "https://snapurl-xrth.onrender.com"

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Build a timestamped filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(UPLOAD_FOLDER, safe_filename)

        # Save the file to disk
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Construct the public URL
        url = f"{BASE_URL}/images/{safe_filename}"

        # Insert into MongoDB
        image_doc = {
            "filename": safe_filename,
            "original_filename": file.filename,
            "url": url,
            "uploaded_at": datetime.utcnow()
        }
        result = await images.insert_one(image_doc)
        image_doc["_id"] = str(result.inserted_id)

        return image_doc

    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/images")
async def get_images():
    try:
        cursor = images.find().sort("uploaded_at", -1)
        image_list = []
        async for image in cursor:
            image["_id"] = str(image["_id"])
            image_list.append(image)
        return image_list
    except Exception as e:
        logger.error(f"Error fetching images: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/images/{image_id}")
async def delete_image(image_id: str):
    try:
        image = await images.find_one({"_id": ObjectId(image_id)})
        if not image:
            raise HTTPException(status_code=404, detail="Image not found")

        # Remove file
        file_path = os.path.join(UPLOAD_FOLDER, image["filename"])
        if os.path.exists(file_path):
            os.remove(file_path)

        # Delete DB record
        await images.delete_one({"_id": ObjectId(image_id)})

        return {"message": "Image deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting image: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health_check():
    try:
        await client.admin.command('ping')
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow(),
            "mongodb": "connected"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    return {"message": "Welcome to SnapURL API. Visit /docs for API documentation."}
