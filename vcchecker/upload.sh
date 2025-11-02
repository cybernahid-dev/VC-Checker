#!/bin/bash
# =========================================================
# 🔄 Universal Auto Upload Script for GitHub (Debug Mode)
# Author: cybernahid-dev
# Year: 2025
# =========================================================

set -e  # Stop on error
set -x  # DEBUG MODE (shows each command as it runs)

# --- 🛠 CONFIGURATION ---
REPO_URL=$(git config --get remote.origin.url)
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")
WATCH_DIR=$(pwd)

# --- ⚡ CHECKS ---
if [ -z "$REPO_URL" ]; then
  echo "❌ No GitHub repository linked. Use:"
  echo "   git remote add origin <repo-url>"
  exit 1
fi

if ! command -v inotifywait &>/dev/null; then
  echo "⚙️ Installing dependency: inotify-tools..."
  pkg install inotify-tools -y >/dev/null 2>&1 || sudo apt install inotify-tools -y
fi

# --- 🚀 AUTO SYNC LOOP ---
echo "🚀 Auto Upload Activated for: $WATCH_DIR"
echo "📡 Watching branch: $BRANCH"
echo "🔐 Repo: $REPO_URL"
echo "-------------------------------------------"

# Check initial connectivity
git fetch origin >/dev/null 2>&1 || echo "⚠️ Warning: Couldn't fetch origin. Check SSH or remote setup."

while true; do
  echo "👀 Watching for changes..."
  inotifywait -r -e modify,create,delete,move $WATCH_DIR
  echo "🔄 Change detected! Uploading to GitHub..."
  git add .
  git commit -m "Auto-update: $(date +"%Y-%m-%d %H:%M:%S")"
  git pull --rebase origin $BRANCH || true
  git push -u origin $BRANCH
  echo "✅ Sync complete at $(date +"%H:%M:%S")"
  echo "-------------------------------------------"
done
