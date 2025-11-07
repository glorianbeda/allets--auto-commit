from fastapi import FastAPI, Request
import subprocess
import google.generativeai as genai
import os

# --- Konfigurasi Gemini API ---
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI(title="AI Commit Server")

# --- Helper untuk ambil diff Git ---
def get_git_diff(repo_path: str) -> str:
    """Ambil perubahan git dari repo_path."""
    try:
        diff = subprocess.check_output(
            ["git", "-C", repo_path, "diff", "--cached"],
            stderr=subprocess.STDOUT
        ).decode("utf-8")
        return diff if diff.strip() else "(Tidak ada perubahan terdeteksi)"
    except subprocess.CalledProcessError as e:
        return f"Error mengambil diff: {e.output.decode('utf-8')}"

# --- Helper untuk generate pesan commit pakai Gemini ---
def generate_commit_message(repo_path: str) -> str:
    """Generate pesan commit berdasarkan perubahan git."""
    diff = get_git_diff(repo_path)

    prompt = f"""
Kamu adalah asisten AI yang membantu membuat pesan commit Git.
Berikut perubahan dalam kode (git diff):

{diff}

Buat pesan commit singkat dan jelas sesuai konvensi Conventional Commit:
- Gunakan format seperti "feat: ", "fix: ", "chore: ", "refactor: ", dll.
- Gunakan Bahasa Inggris.
- Jangan tambahkan kutip atau tanda lain.
Pesan commit:
"""

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        message = response.text.strip()
        # Bersihkan kemungkinan karakter aneh
        message = message.replace('\n', ' ').strip()
        return message
    except Exception as e:
        return f"Error dari Gemini API: {e}"

# --- Endpoint API utama ---
@app.post("/generate-commit-message")
async def generate_commit_message_endpoint(request: Request):
    """Endpoint untuk menerima repo_path dan mengembalikan pesan commit AI."""
    try:
        data = await request.json()
        repo_path = data.get("repo_path", ".")
        message = generate_commit_message(repo_path)
        return {"message": message}
    except Exception as e:
        return {"error": str(e)}

# --- Root Endpoint ---
@app.get("/")
def root():
    return {"status": "AI Commit Server aktif 🚀"}
