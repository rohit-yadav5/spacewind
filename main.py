from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from backend.wordtopdf.converter import router as converter_router
from backend.github_auto_puller import GitAutoPuller
from backend.webhook.handler import router as webhook_router
import os

app = FastAPI()

# Mount static and templates
os.makedirs("converted", exist_ok=True)
app.mount("/converted", StaticFiles(directory="converted"), name="converted")

# Include the Word-to-PDF route
app.include_router(converter_router)

# Include GitHub webhook handler route
app.include_router(webhook_router)

# Auto Git Pull setup (if needed directly here, optional)
REPO_PATH = "/home/rohit/work/github/spacewind"
puller = GitAutoPuller(REPO_PATH)

@app.post("/webhook-direct")
async def webhook_direct(request: Request):
    """Fallback: Direct webhook handler if needed"""
    data = await request.json()
    if data.get("ref") == "refs/heads/main":
        return puller.pull()
    return {"message": "Not main branch, ignored"}
