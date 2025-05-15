@app.route("/run", methods=["GET", "POST"])
def run_script():
    token = request.args.get("token")
    if token != os.getenv("ACCESS_TOKEN"):
        return jsonify({"error": "Invalid token"}), 403

    # ① PlaywrightスクリプトでHTMLを更新
    result1 = subprocess.run(
        ["python", "gamba_fetch_announcement.py"],
        capture_output=True,
        text=True
    )

    # ② 差分チェック＋LINE通知
    result2 = subprocess.run(
        ["python", "check_and_notify.py"],
        capture_output=True,
        text=True
    )

    return jsonify({
        "stdout_fetch": result1.stdout,
        "stderr_fetch": result1.stderr,
        "stdout_notify": result2.stdout,
        "stderr_notify": result2.stderr,
        "returncode_fetch": result1.returncode,
        "returncode_notify": result2.returncode,
    })
