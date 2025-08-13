import shutil
import uuid
import os
import subprocess
from fastapi import UploadFile, APIRouter, File

# Router for main.py
router = APIRouter()

# Get the directory of this file (backend/wordtopdf/)
BASE_DIR = os.path.dirname(__file__)

# Paths for uploads and converted files
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
OUTPUT_DIR = os.path.join(BASE_DIR, "converted")


class WordToPDFConverter:
    def __init__(self, upload_dir: str, output_dir: str):
        self.upload_dir = upload_dir
        self.output_dir = output_dir

        # Ensure directories exist
        os.makedirs(self.upload_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

    async def convert(self, file: UploadFile):
        # Validate file extension
        if not file.filename.lower().endswith(".docx"):
            return {"success": False, "error": "Please upload a .docx file."}

        # Generate unique IDs for input & output
        file_id = str(uuid.uuid4())
        input_path = os.path.join(self.upload_dir, f"{file_id}.docx")
        output_path = os.path.join(self.output_dir, f"{file_id}.pdf")

        # Save uploaded file
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Convert using LibreOffice
        result = subprocess.run(
            [
                "libreoffice", "--headless",
                "--convert-to", "pdf",
                "--outdir", self.output_dir,
                input_path
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Expected LibreOffice output file
        generated_pdf_path = os.path.join(
            self.output_dir,
            os.path.splitext(os.path.basename(input_path))[0] + ".pdf"
        )

        # Rename to our UUID-based filename for consistency
        if os.path.exists(generated_pdf_path):
            os.rename(generated_pdf_path, output_path)
            return {
                "success": True,
                "download_link": f"https://spacewind.xyz/converted/{file_id}.pdf"
            }

        # If conversion failed
        return {
            "success": False,
            "error": f"Conversion failed. Details: {result.stderr.decode().strip()}"
        }


# Create instance
converter_instance = WordToPDFConverter(upload_dir=UPLOAD_DIR, output_dir=OUTPUT_DIR)


@router.post("/convert")
async def convert_docx_to_pdf(file: UploadFile = File(...)):
    return await converter_instance.convert(file)
