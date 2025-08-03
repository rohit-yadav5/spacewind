from fastapi import FastAPI, Request
from pydantic import BaseModel
import subprocess
import uvicorn

class WebhookPayload(BaseModel):
    # You can expand this model if you want to verify specific fields
    ref: str | None = None

class GitHubAutoPuller:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.app = FastAPI()
        self.setup_routes()

    def setup_routes(self):
        @self.app.post("/webhook")
        async def handle_webhook(payload: WebhookPayload, request: Request):
            # Optional: verify GitHub headers or IP here
            print("Webhook received. Pulling latest code...")
            output = self.pull_code()
            return {"status": "success", "output": output}

    def pull_code(self):
        try:
            result = subprocess.check_output(
                ["git", "pull"],
                cwd=self.repo_path,
                stderr=subprocess.STDOUT
            )
            return result.decode()
        except subprocess.CalledProcessError as e:
            return f"Error while pulling: {e.output.decode()}"

def run():
    puller = GitHubAutoPuller(repo_path="/home/rohit/work/github/spacewind")
    uvicorn.run(puller.app, host="0.0.0.0", port=9000)


# github_auto_puller.py

from fastapi import APIRouter, Request

class GitHubWebhookHandler:
    def __init__(self):
        self.router = APIRouter()
        self.router.post("/webhook")(self.webhook)

    async def webhook(self, request: Request):
        payload = await request.json()
        print("Webhook received:", payload.get("head_commit", {}).get("message", "No commit message"))
        return {"status": "ok"}



if __name__ == "__main__":
    run()
