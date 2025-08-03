from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

from converter.word_to_pdf import WordToPDFConverter
from webhook.handler import GitHubWebhookHandler

app = FastAPI()

# Setup templates and static file mounts
templates = Jinja2Templates(directory="templates")
app.mount("/converted", StaticFiles(directory="converted"), name="converted")

# Create required folders
os.makedirs("uploads", exist_ok=True)
os.makedirs("converted", exist_ok=True)

# Instantiate converter
converter = WordToPDFConverter(upload_dir="uploads", output_dir="converted")

@app.get("/", response_class=HTMLResponse)
async def show_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/convert")
async def convert_file(request: Request, file: UploadFile = File(...)):
    result = await converter.convert(file)
    if result["success"]:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "download_link": result["download_link"]
        })
    else:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": result["error"]
        })

# GitHub webhook
webhook_handler = GitHubWebhookHandler(repo_path="/home/rohit/work/github/spacewind")
app.include_router(webhook_handler.router)


print("hi can you see me")