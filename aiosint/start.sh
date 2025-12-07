#!/bin/bash

# start-native.sh
# Starts n8n and the Python Social API natively

cColorRojo='\033[1;31m'
cColorVerde='\033[1;32m'
cFinColor='\033[0m'

INSTALL_DIR="$HOME/aiosint"
VENV_DIR="$INSTALL_DIR/venv"

# Check if venv exists
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${cColorRojo}[!] Virtual environment not found at $VENV_DIR. Please run install-native.sh first.${cFinColor}"
    exit 1
fi

# Load environment variables if they exist
ENV_FILE="$INSTALL_DIR/.env_euskal"
if [ -f "$ENV_FILE" ]; then
    echo -e "${cColorVerde}[+] Loading environment variables from $ENV_FILE${cFinColor}"
    export $(grep -v '^#' "$ENV_FILE" | xargs)
fi

# Start Social API in background
echo -e "${cColorVerde}[+] Starting Social API (background)...${cFinColor}"
source "$VENV_DIR/bin/activate"
nohup python3 "$INSTALL_DIR/n8n/social-api-native.py" > "$INSTALL_DIR/social-api.log" 2>&1 &
API_PID=$!
echo -e "    PID: $API_PID"
deactivate

# Start n8n
echo -e "${cColorVerde}[+] Starting n8n...${cFinColor}"
# Using nohup or just running it? 
# Usually n8n runs in foreground if not detached. 
# Let's run it in foreground so the user can see output, or provide option.
# For this script, let's run it and wait.
# We also need to set some n8n env vars that were in docker-compose
export N8N_COMMUNITY_PACKAGES_ALLOW_TOOL_USAGE=true
export N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=true
export N8N_RUNNERS_ENABLED=true
export N8N_SECURE_COOKIE=false
# Port mapping was 5678:5678, so default is fine.

n8n start

# Kill API when n8n stops
kill $API_PID
