from fastapi import FastAPI, Request
import subprocess
import os

app = FastAPI()

@app.api_route("/run", methods=["GET", "POST", "HEAD"])
async def run_script(request: Request):
    token = request.query_params.get("token")
    if token != os.getenv("ACCESS_TOKEN"):
        return {"error": "Unauthorized"}

    if request.method == "HEAD":
        # 処理をスキップして「正常だよ」とだけ返す
        return {"status": "OK (HEAD method)"}

    result = subprocess.run(["python", "check_and_notify.py"], capture_output=True)
    return {
        "stdout": result.stdout.decode(),
        "stderr": result.stderr.decode(),
        "returncode": result.returncode,
    }
