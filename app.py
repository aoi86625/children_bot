from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import subprocess
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()  # ← これが必要！

@app.get("/")
def read_root():
    return {"message": "Server is running"}

@app.post("/run")
@app.get("/run")
async def run_script(request: Request):
    token = request.query_params.get("token")
    if token != os.getenv("LINE_BOT_TRIGGER_TOKEN"):
        return JSONResponse(status_code=403, content={"error": "Invalid token"})

    result = subprocess.run(["python", "check_and_notify.py"], capture_output=True, text=True)
    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode
    }
