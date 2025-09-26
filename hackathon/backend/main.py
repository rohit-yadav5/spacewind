from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from text_to_video.generator import generate_video_from_text, outputs_dir

app = FastAPI()

class TextRequest(BaseModel):
    text: str

@app.get("/")
def root():
    return {"message": "Backend is running on port 8700 🚀. Go to /docs to test the API."}

@app.post("/generate")
def generate_video(request: TextRequest):
    """
    Generate a sign-language video for the given text.
    """
    try:
        result = generate_video_from_text(request.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Video generation failed: {str(e)}")

    video_path = result.get("video_path")
    processed_chars = result.get("processed_chars")

    if not video_path or not os.path.exists(video_path):
        raise HTTPException(status_code=500, detail="No video was generated or video file not found.")

    return FileResponse(video_path, media_type="video/mp4", filename=os.path.basename(video_path))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8700, reload=True)