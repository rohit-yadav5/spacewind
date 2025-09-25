from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

app = FastAPI()

frontend_path = os.path.join(os.path.dirname(__file__), '../frontend')
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="static")

if __name__ == "__main__":
	uvicorn.run("main:app", host="0.0.0.0", port=8700, reload=True)
