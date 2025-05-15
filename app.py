from fastapi import FastAPI, Request
import subprocess
import os

app = FastAPI()

@app.api_route("/run", methods=["GET", "POST"])
async def run_script(request: Request):
    # 環境変数からトークンを取得
    token = request.query_params.get("token")
    if token != os.getenv("ACCESS_TOKEN"):
        return {"error": "Unauthorized"}

    # check_and_notify.py を実行
    result = subprocess.run(
        ["python", "check_and_notify.py"],
        capture_output=True
    )

    # 実行結果をJSONで返す
    return {
        "stdout": result.stdout.decode(),
        "stderr": result.stderr.decode(),
        "returncode": result.returncode,
    }
