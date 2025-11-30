from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from pathlib import Path
import shutil
from transcription import transcribe_audio
from processing import process_transcript

app = FastAPI(title="IndianMeet AI")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.get("/")
async def root():
    return {"message": "IndianMeet AI - Meeting Assistant for Indians"}

@app.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    """
    Upload audio file and process it
    """
    try:
        # Save uploaded file
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        print(f"File saved: {file_path}")
        
        # Transcribe audio
        print("Starting transcription...")
        transcript = transcribe_audio(str(file_path))
        
        # Process transcript
        print("Processing transcript...")
        result = process_transcript(transcript)
        
        # Cleanup
        os.remove(file_path)
        
        return JSONResponse(content={
            "success": True,
            "transcript": transcript,
            "summary": result["summary"],
            "action_items": result["action_items"],
            "participants": result["participants"]
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process-text")
async def process_text(data: dict):
    """
    Process pre-transcribed text (for testing)
    """
    try:
        transcript = data.get("transcript", "")
        result = process_transcript(transcript)
        
        return JSONResponse(content={
            "success": True,
            "summary": result["summary"],
            "action_items": result["action_items"],
            "participants": result["participants"]
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)