#!/bin/bash

# Script ini akan meng-install hook 'prepare-commit-msg' di repositori Git saat ini.

# 1. Tentukan lokasi folder hooks
HOOKS_DIR=$(git rev-parse --git-dir 2>/dev/null)/hooks
if [ -z "$HOOKS_DIR" ]; then
  echo "❌ Error: Ini bukan repositori Git."
  echo "Harap jalankan skrip ini dari dalam direktori proyek Anda."
  exit 1
fi

# 2. Tentukan nama file hook
HOOK_FILE="$HOOKS_DIR/prepare-commit-msg"

# 3. Cek apakah hook sudah ada
if [ -f "$HOOK_FILE" ]; then
  echo "⚠️  Peringatan: File hook '$HOOK_FILE' sudah ada."
  echo -n "Apakah Anda ingin menimpanya? (y/n): "
  read OVERWRITE </dev/tty
  if [ "$OVERWRITE" != "y" ] && [ "$OVERWRITE" != "Y" ]; then
    echo "Dibatalkan. Tidak ada perubahan."
    exit 1
  fi
  echo "Menimpa file hook..."
fi

# 4. Tulis konten skrip ke dalam file hook
# Menggunakan 'EOF' (dengan tanda kutip) memastikan bahwa karakter $
# tidak diekspansi dan ditulis apa adanya ke dalam file.
cat > "$HOOK_FILE" <<'EOF'
#!/bin/bash

# Jika variabel ini sudah ada, berarti kita berada dalam rekursi. Keluar.
if [ "$AI_COMMIT_IN_PROGRESS" = "true" ]; then
  exit 0
fi

AI_SERVER_URL="http://localhost:8000/generate-commit-message"
REPO_PATH=$(git rev-parse --show-toplevel)

if [ -z "$REPO_PATH" ]; then
  echo "⚠️ Bukan repositori Git. Membatalkan hook."
  exit 1
fi

# Kirim path repo sebagai JSON
AI_MESSAGE=$(curl -s -X POST -H "Content-Type: application/json" -d "{\"repo_path\": \"$REPO_PATH\"}" "$AI_SERVER_URL" | jq -r '.message')

# Cek jika AI_MESSAGE kosong atau "null" (dari jq) atau mengandung error
if [ -z "$AI_MESSAGE" ] || [ "$AI_MESSAGE" = "null" ] || [[ "$AI_MESSAGE" == Error* ]]; then
  echo "⚠️ Gagal mendapatkan pesan dari AI server."
  echo "Server response: $AI_MESSAGE"
  # Izinkan pengguna menulis pesan manual
  exit 0
fi

echo ""
echo "----------------------------------"
echo "Pesan AI: $AI_MESSAGE"
echo "----------------------------------"
echo -n "Gunakan pesan ini untuk commit? (y/n): "
read CONFIRM </dev/tty

if [ "$CONFIRM" = "y" ] || [ "$CONFIRM" = "Y" ] || [ -z "$CONFIRM" ]; then
  # Set variabel untuk mencegah rekursi dari hook commit
  export AI_COMMIT_IN_PROGRESS="true"

  # Lakukan commit langsung menggunakan pesan dari AI
  git commit -m "$AI_MESSAGE"

  # Cek status exit dari perintah commit
  if [ $? -eq 0 ]; then
    echo "✅ Commit berhasil dibuat."
  else
    echo "❌ Gagal membuat commit. Mungkin ada masalah lain (seperti pre-commit hook lain yang gagal)."
    # Keluar dengan 0 agar tidak ada pesan error aneh dari hook
    exit 0
  fi

  # Keluar dengan non-zero untuk membatalkan proses 'git commit' asli yang memicu hook ini
  exit 1
else
  echo "❌ Pesan AI dibatalkan. Silakan tulis pesan manual di editor."

  # Cek apakah editor Git sudah dikonfigurasi untuk mencegah error
  GIT_EDITOR=$(git config core.editor)
  if [ -z "$GIT_EDITOR" ]; then
    echo ""
    echo "⚠️  Peringatan: Editor Git default tidak ditemukan."
    echo "    Untuk dapat menulis pesan manual, jalankan perintah berikut:"
    echo "    git config --global core.editor nano"
    echo "    (Ganti 'nano' dengan editor favorit Anda seperti 'vim' atau 'code --wait')"
    echo ""
    echo "    Commit dibatalkan."
    exit 1 # Batalkan commit untuk menghindari error dari Git
  fi

  # Keluar dengan 0 agar editor tetap terbuka untuk input manual
  exit 0
fi
EOF

# 5. Atur hak akses file agar executable
chmod +x "$HOOK_FILE"

echo ""
echo "✅ Sukses!"
echo "Git hook telah di-install di:"
echo "$HOOK_FILE"
echo "Hak akses execute telah diatur."
