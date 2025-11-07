#!/usr/bin/env python3
import google.generativeai as genai
import os
from utils import load_config  # kita pakai util dari project sebelumnya

def test_gemini():
    """Tes apakah koneksi ke Gemini API berhasil."""
    try:
        config = load_config()
        api_key = config.get("gemini_api_key")

        if not api_key:
            print("❌ API key tidak ditemukan di config.yaml")
            return

        # Konfigurasi Gemini
        genai.configure(api_key=api_key)

        # Coba panggil model sederhana
        model_name = config.get("model", "gemini-2.5-flash")
        model = genai.GenerativeModel(model_name)

        prompt = "Katakan 'Halo dunia' dalam bahasa Indonesia, arab, dan yunani."
        response = model.generate_content(prompt)

        print("✅ Koneksi ke Gemini API berhasil!")
        print("🧠 Model:", model_name)
        print("💬 Respons:", response.text.strip())

    except Exception as e:
        print("❌ Gagal terhubung ke Gemini API.")
        print("Error:", e)


if __name__ == "__main__":
    test_gemini()
