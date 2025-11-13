from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import subprocess
import google.generativeai as genai
import os

# ======================================================
# 🔧 Load environment (.env) dan konfigurasi Gemini
# ======================================================
load_dotenv()  # baca file .env di direktori kerja
api_key = os.getenv("GEMINI_API_KEY")
model_name = os.getenv("MODEL", "gemini-1.5-flash-latest")  # default model

if not api_key:
    raise ValueError(
        "❌ GEMINI_API_KEY tidak ditemukan.\n"
        "Pastikan file .env ada dan berisi:\n\n"
        "GEMINI_API_KEY=YOUR_API_KEY\n"
    )

# Konfigurasi API key Gemini
genai.configure(api_key=api_key)

# ======================================================
# 🚀 Inisialisasi FastAPI
# ======================================================
app = FastAPI(title="AI Commit Server")

# ======================================================
# 🧠 Fungsi bantu
# ======================================================
def get_git_diff(repo_path: str) -> str:
    """Ambil perubahan dari file yang sudah di-stage (git add)."""
    try:
        diff = subprocess.check_output(
            ["git", "-C", repo_path, "diff", "--cached"],
            stderr=subprocess.STDOUT
        ).decode("utf-8")
        return diff.strip() or "(Tidak ada perubahan di stage)"
    except subprocess.CalledProcessError as e:
        return f"Error mengambil diff: {e.output.decode('utf-8')}"


def generate_commit_message(repo_path: str) -> str:
    """Generate pesan commit menggunakan Gemini berdasarkan diff."""
    diff = get_git_diff(repo_path)
    prompt = f"""
Kamu adalah asisten AI yang membantu membuat pesan commit Git.
Berikut perubahan dalam kode (git diff):

{diff}

Buat pesan commit singkat dan jelas sesuai konvensi Conventional Commit:
- Gunakan format seperti "feat: ", "fix: ", "refactor: ", "chore: ", dll.
- Gunakan Bahasa Inggris.
- Jangan tambahkan tanda kutip.
Hanya berikan 1 baris pesan commit.
Pesan commit:
"""
    try:
        model_instance = genai.GenerativeModel(model_name)
        response = model_instance.generate_content(prompt)
        message = response.text.strip().replace("\n", " ")
        return message
    except Exception as e:
        return f"Error dari Gemini API: {e}"

# ======================================================
# 🧩 Endpoint API
# ======================================================
@app.post("/generate-commit-message")
async def generate_commit_message_endpoint(request: Request):
    """Endpoint untuk menerima path repo dan mengembalikan pesan commit."""
    try:
        data = await request.json()
        repo_path = data.get("repo_path", ".")
        message = generate_commit_message(repo_path)
        return JSONResponse(content={"message": message})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/")
def root():
    """Cek status server."""
    return {"status": "✅ AI Commit Server aktif dan siap digunakan."}
