from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import shutil
import os
import uuid
from sqlalchemy.orm import Session

from .enhancer import apply_filter
from . import database, models, auth

# Create Database Tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Constants
UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
TEMPLATES_DIR = "templates"

# Ensure directories exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Include Auth Router
app.include_router(auth.router)

# Mount Static Files
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- Page Routes ---

@app.get("/")
def read_root():
    return FileResponse(os.path.join(TEMPLATES_DIR, "landing.html"))

@app.get("/login")
def login_page():
    return FileResponse(os.path.join(TEMPLATES_DIR, "login.html"))

@app.get("/register")
def register_page():
    return FileResponse(os.path.join(TEMPLATES_DIR, "register.html"))

@app.get("/dashboard")
def dashboard_page():
    return FileResponse(os.path.join(TEMPLATES_DIR, "dashboard.html"))

# --- Protected Enhance Route ---

@app.post("/enhance")
def enhance_image(
    file: UploadFile = File(...), 
    filter_type: str = Form(...),
    width: int = Form(None),
    height: int = Form(None),
    current_user: models.User = Depends(auth.get_current_user), # Protected Route
    db: Session = Depends(database.get_db)
):
    # Validate file type
    if file.filename.split(".")[-1].lower() not in ["jpg", "jpeg", "png"]:
         raise HTTPException(status_code=400, detail="Invalid file type. Only JPG, JPEG, PNG are supported.")

    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    upload_path = os.path.join(UPLOAD_DIR, unique_filename)
    output_filename = f"enhanced_{unique_filename}"
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    # Save uploaded file
    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Process image
        apply_filter(upload_path, filter_type, output_path, params={"width": width, "height": height})
        
        # Save to History
        history_item = models.ImageHistory(
            user_id=current_user.id,
            original_filename=unique_filename,
            enhanced_filename=output_filename
        )
        db.add(history_item)
        db.commit()
        db.refresh(history_item)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    # Return processed file
    return FileResponse(output_path, media_type="image/jpeg", filename=output_filename)

# --- History Routes ---

@app.get("/history")
def get_user_history(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    history_items = db.query(models.ImageHistory).filter(models.ImageHistory.user_id == current_user.id).order_by(models.ImageHistory.timestamp.desc()).all()
    return [{
        "id": item.id,
        "original_filename": item.original_filename,
        "enhanced_filename": item.enhanced_filename,
        "timestamp": item.timestamp.isoformat()
    } for item in history_items]

@app.get("/uploads/{filename}")
def get_upload(filename: str):
    path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(path):
        return FileResponse(path)
    return HTTPException(status_code=404)

@app.get("/outputs/{filename}")
def get_output(filename: str):
    path = os.path.join(OUTPUT_DIR, filename)
    if os.path.exists(path):
        return FileResponse(path)
    return HTTPException(status_code=404)


if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
