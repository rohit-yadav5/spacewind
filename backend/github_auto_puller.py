import os
import subprocess
import logging

class GitAutoPuller:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[logging.StreamHandler()]
        )

    def pull(self):
        logging.info(f"Trying to pull latest changes in: {self.repo_path}")
        try:
            result = subprocess.run(
                ["git", "pull"],
                cwd=self.repo_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode == 0:
                logging.info("Git pull successful.")
                logging.info(result.stdout)
                return {"status": "success", "details": result.stdout}
            else:
                logging.error("Git pull failed.")
                logging.error(result.stderr)
                return {"status": "error", "details": result.stderr}
        except Exception as e:
            logging.exception("Exception occurred while pulling repo.")
            return {"status": "error", "details": str(e)}

#v1 main release