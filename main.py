from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import shutil
import os
import subprocess
import uuid
from github_auto_puller import GitHubWebhookHandler

app = FastAPI()
handler = GitHubWebhookHandler()
app.include_router(handler.router)

# Create folders if not exist
os.makedirs("uploads", exist_ok=True)
os.makedirs("converted", exist_ok=True)

app.mount("/converted", StaticFiles(directory="converted"), name="converted")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/convert")
async def convert_to_pdf(request: Request, file: UploadFile = File(...)):
    if not file.filename.endswith(".docx"):
        return templates.TemplateResponse("index.html", {"request": request, "error": "Please upload a .docx file."})

    file_id = str(uuid.uuid4())
    input_path = f"uploads/{file_id}.docx"
    output_path = f"converted/{file_id}.pdf"

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Convert using LibreOffice (must be installed)
    subprocess.run(["libreoffice", "--headless", "--convert-to", "pdf", "--outdir", "converted", input_path])

    if os.path.exists(output_path):
        return templates.TemplateResponse("index.html", {
            "request": request,
            "download_link": f"/converted/{file_id}.pdf"
        })
    else:
        return templates.TemplateResponse("index.html", {"request": request, "error": "Conversion failed."})

@app.post("/webhook")
async def handle_webhook(request: Request):
    payload = await request.json()
    print("Received webhook:", payload)
    return {"status": "ok"}