from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import subprocess
import os

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
@app.head("/", response_class=HTMLResponse)  # ← HEAD対応を追加！
async def root():
    return "<h1>Children Bot is running.</h1>"

@app.post("/run")
async def run_check_and_notify(request: Request):
    token = request.query_params.get("token")
    if token != os.getenv("LINE_BOT_TOKEN"):
        return {"error": "Unauthorized"}

    process = subprocess.run(["python", "check_and_notify.py"], capture_output=True, text=True)
    return {
        "stdout": process.stdout,
        "stderr": process.stderr,
        "returncode": process.returncode,
    }
