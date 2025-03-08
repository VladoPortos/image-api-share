import os
import uuid
import shutil
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Header, HTTPException, Response
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Configuration from environment variables
API_KEY = os.environ.get("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable must be set")

BASE_URL = os.environ.get("BASE_URL", "http://localhost")

# Create storage directory if it doesn't exist
UPLOAD_DIR = "/app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(title="Image Share API")

class ImageResponse(BaseModel):
    image_id: str
    download_url: str

def validate_api_key(api_key: Optional[str] = Header(None)):
    if not api_key or api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return api_key

@app.get("/")
async def root():
    return {"message": "Image Share API", "version": "1.0.0"}

@app.put("/images", response_model=ImageResponse)
async def upload_image(
    file: UploadFile = File(...),
    api_key: str = Header(...)
):
    validate_api_key(api_key)
    
    # Validate file is an image
    content_type = file.content_type
    if not content_type or not content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Generate unique ID and determine file extension
    image_id = str(uuid.uuid4())
    file_extension = os.path.splitext(file.filename)[1] if file.filename else ""
    filename = f"{image_id}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    # Save the file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Return the download URL
    download_url = f"{BASE_URL}/images/{filename}"
    return ImageResponse(image_id=image_id, download_url=download_url)

@app.get("/images/{filename}")
async def get_image(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(file_path)

@app.delete("/images/{filename}")
async def delete_image(filename: str, api_key: str = Header(...)):
    validate_api_key(api_key)
    
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")
    
    # Delete the file
    os.remove(file_path)
    return Response(status_code=204)

# Mount static files for serving images directly
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")
