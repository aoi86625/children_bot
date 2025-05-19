from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import subprocess
import os

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
@app.head("/", response_class=HTMLResponse)
async def root():
    return "<h1>Children Bot is running.</h1>"

@app.post("/run")
@app.head("/run")  # ← ここを追加！
async def run_check_and_notify(request: Request = None):
    # HEADリクエスト時は処理せず200だけ返す
    if request and request.method == "HEAD":
        return {"status": "ok"}

    token = request.query_params.get("token")
    if token != os.getenv("LINE_BOT_TOKEN"):
        return {"error": "Unauthorized"}

    process = subprocess.run(["python", "check_and_notify.py"], capture_output=True, text=True)
    return {
        "stdout": process.stdout,
        "stderr": process.stderr,
        "returncode": process.returncode,
    }
