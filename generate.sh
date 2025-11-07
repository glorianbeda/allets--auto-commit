#!/bin/bash
# ==========================================================
# 🚀 AI Commit Hook Installer (Stable Non-Recursive Version)
# ==========================================================
# Script ini membuat hook .git/hooks/prepare-commit-msg
# untuk integrasi AI Commit Generator (misalnya main.py)
# ----------------------------------------------------------

HOOK_PATH=".git/hooks/prepare-commit-msg"
AI_COMMIT_SCRIPT="$(pwd)/main.py"

# 1️⃣ Pastikan folder .git ada
if [ ! -d ".git" ]; then
  echo "❌ Folder .git tidak ditemukan. Jalankan script ini di root repo Git."
  exit 1
fi

# 2️⃣ Buat hook file baru
cat > "$HOOK_PATH" <<'EOF'
#!/bin/bash
# ==========================================================
# 🧠 AI Commit Hook — Non-Recursive Safe Version
# ==========================================================

AI_COMMIT_SCRIPT="$(pwd)/main.py"

# Hindari loop
if [ "$AI_COMMIT_RUNNING" = "1" ]; then
  exit 0
fi
export AI_COMMIT_RUNNING=1

# Jalankan AI commit generator
AI_MESSAGE=$(python3 "$AI_COMMIT_SCRIPT")

# Cek error
if [ $? -ne 0 ] || [ -z "$AI_MESSAGE" ]; then
  echo "⚠️ Gagal generate pesan AI."
  exit 1
fi

# Tampilkan hasil
echo ""
echo "----------------------------------"
echo "$AI_MESSAGE"
echo "----------------------------------"
echo -n "Gunakan pesan ini untuk commit? (y/n): "
read CONFIRM </dev/tty

# Konfirmasi user
if [ "$CONFIRM" = "y" ] || [ "$CONFIRM" = "Y" ]; then
  echo "$AI_MESSAGE" > "$1"   # <-- tulis pesan ke file commit Git
  echo "✅ Pesan commit AI diterapkan."
else
  echo "❌ Commit dibatalkan oleh pengguna."
  exit 1
fi
EOF

# 3️⃣ Jadikan executable
chmod +x "$HOOK_PATH"

# 4️⃣ Pesan hasil
if [ -f "$AI_COMMIT_SCRIPT" ]; then
  echo "✅ Hook AI Commit berhasil dipasang!"
  echo "📂 Lokasi hook: $HOOK_PATH"
else
  echo "⚠️ main.py tidak ditemukan — pastikan AI generator kamu ada di sini:"
  echo "   $AI_COMMIT_SCRIPT"
fi
