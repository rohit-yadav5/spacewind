from fastapi import APIRouter, Request
import subprocess

class GitHubWebhookHandler:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.router = APIRouter()
        self.router.post("/webhook")(self.webhook)

    async def webhook(self, request: Request):
        payload = await request.json()

        # Only pull if pushed to main branch
        if payload.get("ref") != "refs/heads/main":
            return {"message": "Not main branch. Ignored."}

        result = self.pull_latest()
        return {"message": result}

    def pull_latest(self):
        try:
            output = subprocess.check_output(["git", "pull"], cwd=self.repo_path)
            return output.decode("utf-8")
        except subprocess.CalledProcessError as e:
            return f"Error during pull: {e.output.decode('utf-8')}"
