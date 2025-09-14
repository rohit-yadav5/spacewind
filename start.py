import subprocess
import os
import sys
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def run_cloudflare():
    """Run Cloudflare Tunnel from home directory"""
    home_dir = os.path.expanduser("~")
    subprocess.Popen(
        ["cloudflared", "tunnel", "run", "spacewind-tunnel"],
        cwd=home_dir
    )
    print("🌐 Cloudflare Tunnel started")

def run_fastapi():
    """Run FastAPI app with uvicorn"""
    project_dir = "/work/github/spacewind"
    subprocess.Popen(
        ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8500"],
        cwd=project_dir
    )
    print("🚀 FastAPI server started at http://0.0.0.0:8500")

def run_portfolio():
    """Run portfolio static server"""
    portfolio_path = os.path.join(BASE_DIR, "rohit")
    if os.path.exists(portfolio_path):
        subprocess.Popen([sys.executable, "-m", "http.server", "5505"], cwd=portfolio_path)
        print(f"🖼 Portfolio server started at http://localhost:5505")
    else:
        print("⚠ Portfolio folder not found")

if __name__ == "__main__":
    print("==== Starting Spacewind Services ====")
    run_cloudflare()
    time.sleep(2)  # small delay for stability
    run_fastapi()
    time.sleep(1)
    run_portfolio()
    print("✅ All services launched successfully")