from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
import os
import subprocess
import sys





# === Feature Flags ===
RUN_WORDTOPDF = True
RUN_FRONTEND = True
RUN_PORTFOLIO = True





BASE_DIR = os.path.dirname(os.path.abspath(__file__))




# Conditional imports
BACKEND_DIR = os.path.join(BASE_DIR, "main_sapacewind", "backend")
sys.path.append(BACKEND_DIR)

if RUN_WORDTOPDF:
    from wordtopdf.converter import router as converter_router
if RUN_FRONTEND:
    from webhook.handler import router as webhook_router

from github_auto_puller import GitAutoPuller

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
    converted_path = os.path.join(BACKEND_DIR, "wordtopdf", "converted")
    os.makedirs(converted_path, exist_ok=True)
    app.mount("/converted", StaticFiles(directory=converted_path), name="converted")
    app.include_router(converter_router)
    print("\n✅ Word-to-PDF feature: ENABLED")
else:
    print("\n❌ Word-to-PDF feature: DISABLED")





# === Frontend setup ===
if RUN_FRONTEND:
    frontend_path = os.path.join(BASE_DIR, "main_sapacewind", "frontend")
    app.include_router(webhook_router)
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
    print("\n✅ Frontend feature: ENABLED")
else:
    print("\n❌ Frontend feature: DISABLED")





# === Portfolio feature setup ===
if RUN_PORTFOLIO:
    portfolio_path = os.path.join(BASE_DIR, "rohit")
    if os.path.exists(portfolio_path):
        print(f"\n✅ Portfolio feature: ENABLED (Serving {portfolio_path} on port 5005)")
        subprocess.Popen(
            ["python3", "-m", "http.server", "5505"],
            cwd=portfolio_path
        )
    else:
        print(f"\n⚠ Portfolio folder not found: {portfolio_path}")
else:
    print("\n❌ Portfolio feature: DISABLED")





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

# v1 main release