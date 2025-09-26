from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os

from text_to_video.generator import generate_video_from_text

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
        # Call the generate_video_from_text function directly
        generate_video_from_text(request.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Video generation failed: {str(e)}")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    video_dir = os.path.abspath(os.path.join(current_dir, "..", "text_to_video", "outputs"))
    if not os.path.exists(video_dir):
        raise HTTPException(status_code=500, detail="Video output directory does not exist.")

    videos = [f for f in os.listdir(video_dir) if f.startswith("output") and f.endswith(".mp4")]
    if not videos:
        raise HTTPException(status_code=500, detail="No video was generated.")

    videos.sort(key=lambda x: os.path.getmtime(os.path.join(video_dir, x)), reverse=True)
    latest_video = os.path.join(video_dir, videos[0])
    return FileResponse(latest_video, media_type="video/mp4", filename=videos[0])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8700, reload=True)