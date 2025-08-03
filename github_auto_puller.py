# github_auto_puller.py

from fastapi import APIRouter, Request
import subprocess

class GitHubWebhookHandler:
    def __init__(self):
        self.router = APIRouter()
        self.router.post("/webhook")(self.webhook)

    async def webhook(self, request: Request):
        try:
            payload = await request.json()
            commit_msg = payload.get("head_commit", {}).get("message", "No commit message")
            print(f"Webhook received: {commit_msg}")

            # Pull the latest changes
            subprocess.run(["git", "pull"], check=True)
            return {"status": "pulled", "commit": commit_msg}

        except Exception as e:
            print("Error handling webhook:", str(e))
            return {"status": "error", "details": str(e)}
