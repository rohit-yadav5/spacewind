from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
import os





# === Feature Flags ===
RUN_WORDTOPDF = True
RUN_FRONTEND = True





# Conditional imports
if RUN_WORDTOPDF:
    from backend.wordtopdf.converter import router as converter_router
if RUN_FRONTEND:
    from backend.webhook.handler import router as webhook_router

from backend.github_auto_puller import GitAutoPuller

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace "*" with ["http://127.0.0.1:5500"] for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





# === Word-to-PDF setup ===
if RUN_WORDTOPDF:
    converted_path = os.path.join("backend", "wordtopdf", "converted")
    os.makedirs(converted_path, exist_ok=True)
    app.mount("/converted", StaticFiles(directory=converted_path), name="converted")
    app.include_router(converter_router)
    print("\n✅ Word-to-PDF feature: ENABLED")
else:
    print("\n❌ Word-to-PDF feature: DISABLED")





# === Frontend setup ===
if RUN_FRONTEND:
    # Serve webhook routes
    app.include_router(webhook_router)
    # Serve static HTML/CSS/JS from the 'frontend' folder
    app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
    print("\n✅ Frontend feature: ENABLED")
else:
    print("\n❌ Frontend feature: DISABLED")










# === Git auto-puller setup ===
REPO_PATH = "/home/rohit/work/github/spacewind"
puller = GitAutoPuller(REPO_PATH)

@app.post("/webhook-direct")
async def webhook_direct(request: Request):
    """Fallback: Direct webhook handler if needed"""
    data = await request.json()
    if data.get("ref") == "refs/heads/main":
        return puller.pull()
    return {"message": "Not main branch, ignored"}
