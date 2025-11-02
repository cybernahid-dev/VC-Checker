#!/bin/bash
# =========================================================
# 🔄 Universal Auto Upload Script (Live Status Edition)
# Author: cybernahid-dev | 2025
# Works with any GitHub project via SSH or HTTPS.
# =========================================================

# --- ⚙️ CONFIGURATION ---
WATCH_DIR=$(pwd)
REPO_URL=$(git config --get remote.origin.url)
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")

# --- 🎨 COLORS ---
GREEN="\e[32m"
RED="\e[31m"
YELLOW="\e[33m"
BLUE="\e[36m"
BOLD="\e[1m"
RESET="\e[0m"

# --- 🧠 FUNCTION: LOGGING ---
log() {
  local type="$1"
  local msg="$2"
  local color="$3"
  echo -e "${color}[${type}]${RESET} ${msg}"
}

# --- ✅ INITIAL CHECKS ---
clear
echo -e "${BOLD}🚀 Auto Upload Activated for:${RESET} $WATCH_DIR"
echo -e "${BOLD}📡 Branch:${RESET} $BRANCH"
echo -e "${BOLD}🔐 Repo:${RESET} $REPO_URL"
echo "-------------------------------------------"

if [ -z "$REPO_URL" ]; then
  log "❌ ERROR" "No GitHub repository linked! Run: git remote add origin <repo-url>" "$RED"
  exit 1
fi

if ! command -v inotifywait &>/dev/null; then
  log "⚙️ INFO" "Installing inotify-tools dependency..." "$YELLOW"
  pkg install inotify-tools -y >/dev/null 2>&1 || sudo apt install inotify-tools -y
  log "✅ DONE" "inotify-tools installed successfully." "$GREEN"
fi

# --- 🧠 VERIFY CONNECTION ---
git fetch origin >/dev/null 2>&1
if [ $? -ne 0 ]; then
  log "❌ ERROR" "Cannot reach GitHub repo. Check SSH/HTTPS access." "$RED"
  exit 1
else
  log "🔗 CONNECTED" "GitHub repository connection OK." "$GREEN"
fi

# --- 🔁 AUTO MONITOR LOOP ---
echo -e "\n👀 ${BOLD}Watching for file changes...${RESET}"
echo "-------------------------------------------"

while true; do
  inotifywait -r -e modify,create,delete,move "$WATCH_DIR" >/dev/null 2>&1
  log "🔄 CHANGE" "File modification detected!" "$BLUE"
  
  git add .
  git commit -m "Auto-update: $(date +"%Y-%m-%d %H:%M:%S")" >/dev/null 2>&1
  if [ $? -eq 0 ]; then
    log "💾 COMMIT" "Local changes committed successfully." "$GREEN"
  else
    log "⚠️ WARNING" "No new changes to commit." "$YELLOW"
  fi

  git push -u origin "$BRANCH" >/dev/null 2>&1
  if [ $? -eq 0 ]; then
    log "🚀 UPLOAD" "Changes synced to GitHub successfully ✅" "$GREEN"
  else
    log "❌ ERROR" "Push failed! Check internet or GitHub access." "$RED"
  fi

  echo "-------------------------------------------"
done
