import shutil
import uuid
import os
import subprocess
from fastapi import UploadFile

class WordToPDFConverter:
    def __init__(self, upload_dir: str, output_dir: str):
        self.upload_dir = upload_dir
        self.output_dir = output_dir

    async def convert(self, file: UploadFile):
        if not file.filename.endswith(".docx"):
            return {"success": False, "error": "Please upload a .docx file."}

        file_id = str(uuid.uuid4())
        input_path = os.path.join(self.upload_dir, f"{file_id}.docx")
        output_path = os.path.join(self.output_dir, f"{file_id}.pdf")

        # Save uploaded file
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Convert using LibreOffice
        subprocess.run(["libreoffice", "--headless", "--convert-to", "pdf", "--outdir", self.output_dir, input_path])

        if os.path.exists(output_path):
            return {
                "success": True,
                "download_link": f"/converted/{file_id}.pdf"
            }
        else:
            return {
                "success": False,
                "error": "Conversion failed."
            }
