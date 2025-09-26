from fastapi import FastAPI
from fastapi.responses import FileResponse
import os
import subprocess

app = FastAPI()

# Path to your text_to_video generator script
GENERATOR_SCRIPT = os.path.join(os.path.dirname(__file__), "../text_to_video/generator.py")

@app.get("/")
def root():
    return {"message": "Backend is running on port 8700 🚀. Go to /docs to test the API."}

@app.get("/generate")
def generate_video(text: str):
    """
    Generate a sign-language video for the given text.
    Example: /generate?text=hello thankyou
    """
    # Run generator.py with subprocess, passing input text
    process = subprocess.run(
        ["python", GENERATOR_SCRIPT],
        input=text,
        text=True,
        capture_output=True
    )

    if process.returncode != 0:
        return {"error": process.stderr}

    # Since generator saves output as outputN.mp4, find the latest file
    video_dir = os.path.join(os.path.dirname(__file__), "../text_to_video")
    videos = [f for f in os.listdir(video_dir) if f.startswith("output") and f.endswith(".mp4")]
    videos.sort(key=lambda x: os.path.getmtime(os.path.join(video_dir, x)), reverse=True)

    if not videos:
        return {"error": "No video was generated."}

    latest_video = os.path.join(video_dir, videos[0])
    return FileResponse(latest_video, media_type="video/mp4", filename=videos[0])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8700, reload=True)