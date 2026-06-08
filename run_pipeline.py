from fastapi import FastAPI, Request
import subprocess
import hmac
import hashlib

app = FastAPI()

GITHUB_SECRET = "your_secret_here"

def verify_signature(payload_body, signature):
    mac = hmac.new(GITHUB_SECRET.encode(), msg=payload_body, digestmod=hashlib.sha256)
    expected = "sha256=" + mac.hexdigest()
    return hmac.compare_digest(expected, signature)

@app.post("/webhook")
async def github_webhook(request: Request):
    body = await request.body()
    signature = request.headers.get("X-Hub-Signature-256")

    if not verify_signature(body, signature):
        return {"error": "invalid signature"}

    event = request.headers.get("X-GitHub-Event")

    if event == "push":
        print("🚀 GitHub push detected — running pipeline...")

        # run your automation script
        subprocess.Popen(["python", "run_pipeline.py"])

    return {"status": "ok"}
