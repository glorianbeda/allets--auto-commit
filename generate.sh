#!/bin/bash
# ==========================================================
# 🔥 AI Commit Hook Installer
# ==========================================================
# Script ini membuat .git/hooks/prepare-commit-msg otomatis
# yang terhubung ke main.py (AI Commit Generator)
# ----------------------------------------------------------

HOOK_PATH=".git/hooks/prepare-commit-msg"
AI_COMMIT_SCRIPT="$(pwd)/main.py"

# Pastikan folder .git ada
if [ ! -d ".git" ]; then
  echo "❌ Folder .git tidak ditemukan. Jalankan script ini di root repo Git."
  exit 1
fi

# Buat hook file baru
cat > "$HOOK_PATH" <<'EOF'
#!/bin/bash
# ==========================================================
# 🧠 AI Commit Hook (auto commit + loop protection)
# ==========================================================

# Cegah infinite loop
if [ "$AI_COMMIT_RUNNING" = "1" ]; then
  exit 0
fi
export AI_COMMIT_RUNNING=1

AI_COMMIT_SCRIPT="$(pwd)/main.py"

# Jalankan AI Commit generator
AI_MESSAGE=$(python3 "$AI_COMMIT_SCRIPT")

# Kalau sukses dan pesan tidak kosong
if [ $? -eq 0 ] && [ ! -z "$AI_MESSAGE" ]; then
  echo ""
  echo "----------------------------------"
  echo "$AI_MESSAGE"
  echo "----------------------------------"
  echo -n "Gunakan pesan ini untuk commit? (y/n): "
  read CONFIRM </dev/tty

  if [ "$CONFIRM" = "y" ] || [ "$CONFIRM" = "Y" ]; then
    echo "✅ Membuat commit otomatis..."
    AI_COMMIT_RUNNING=1 git commit --no-verify --no-edit -m "$AI_MESSAGE"
    echo "✅ Commit otomatis berhasil dengan pesan AI."
    exit 0
  else
    echo "❌ Commit dibatalkan oleh pengguna."
    exit 1
  fi
else
  echo "⚠️ Gagal generate pesan AI."
  exit 1
fi
EOF

# Ubah permission agar bisa dieksekusi
chmod +x "$HOOK_PATH"

# Cek apakah main.py ada
if [ ! -f "main.py" ]; then
  echo "⚠️ main.py tidak ditemukan. Pastikan file generator AI ada di root project."
else
  echo "✅ Hook prepare-commit-msg berhasil dibuat dan siap digunakan!"
fi

echo "📂 Lokasi hook: $HOOK_PATH"
