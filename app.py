from fastapi import FastAPI, Request
import subprocess
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("EXECUTION_TOKEN")

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "OK"}

@app.api_route("/run", methods=["GET", "POST", "HEAD"])
async def run_script(request: Request):
    token = request.query_params.get("token")
    if token != TOKEN:
        return {"error": "Invalid token"}

    process = subprocess.Popen(
        ["python", "check_and_notify.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    return {
        "stdout": stdout.decode("utf-8"),
        "stderr": stderr.decode("utf-8"),
        "returncode": process.returncode
    }
