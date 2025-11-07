from fastapi import FastAPI, Request
import subprocess
import google.generativeai as genai
import os

app = FastAPI()

# Konfigurasi Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

@app.post("/generate-commit-message")
async def generate_commit_message(request: Request):
    data = await request.json()
    repo_path = data.get("repo_path", ".")

    # Ambil diff dari repo (staged files)
    diff = subprocess.run(
        ["git", "-C", repo_path, "diff", "--cached"],
        capture_output=True,
        text=True
    ).stdout

    if not diff.strip():
        return {"message": "No staged changes."}

    # Generate commit message pakai Gemini
    prompt = f"""
    You are a helpful assistant that writes concise and conventional commit messages.
    Based on this git diff, write a short message (max 100 chars):

    {diff}
    """
    response = model.generate_content(prompt)
    commit_message = response.text.strip()

    return {"message": commit_message}
