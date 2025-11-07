#!/usr/bin/env python3
import sys
import subprocess
import google.generativeai as genai
from utils import load_config


def get_staged_diff() -> str:
    """Ambil perubahan file yang sudah di-staged."""
    diff = subprocess.getoutput("git diff --staged")
    if not diff.strip():
        print("⚠️  Tidak ada perubahan yang di-staged.")
        sys.exit(0)
    return diff


def generate_commit_message(diff: str) -> str:
    """Kirim diff ke Gemini dan dapatkan commit message."""
    config = load_config()
    genai.configure(api_key=config["gemini_api_key"])
    model = genai.GenerativeModel(config.get("model", "gemini-1.5-flash"))

    prompt = f"""
    You are a helpful assistant that writes concise Git commit messages.
    Follow Conventional Commits style (feat:, fix:, chore:, refactor:, docs:, test:).
    Based on the diff below, write a clear and meaningful commit message.

    Git diff:
    {diff}
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"❌ Gagal generate pesan: {e}")
        sys.exit(1)


def confirm_and_commit(message: str):
    """Tampilkan pesan commit dan minta konfirmasi user."""
    print("\n✨ Pesan commit yang dihasilkan AI:")
    print("----------------------------------")
    print(message)
    print("----------------------------------")
    confirm = input("Gunakan pesan ini? (y/n): ").lower()

    if confirm == "y":
        subprocess.run(["git", "commit", "-m", message])
        print("✅ Commit berhasil!")
    else:
        print("❌ Commit dibatalkan.")
        sys.exit(1)


if __name__ == "__main__":
    diff = get_staged_diff()
    message = generate_commit_message(diff)
    confirm_and_commit(message)
