#!/bin/bash

# install-native.sh
# Installs OSINT framework (n8n, Maigret, Sherlock, Holehe) natively on Debian 13.

# Colors for output
cColorRojo='\033[1;31m'
cColorVerde='\033[1;32m'
cFinColor='\033[0m'

echo -e "${cColorVerde}[+] Starting native installation for Debian 13...${cFinColor}"

# 1. Update and install system dependencies
echo -e "${cColorVerde}[+] Updating system and installing base dependencies...${cFinColor}"
sudo apt-get update
sudo apt-get install -y curl git python3-full python3-pip python3-venv nodejs npm build-essential libffi-dev libssl-dev zlib1g-dev

# 2. Setup Directory Structure
echo -e "${cColorVerde}[+] Setting up directory structure...${cFinColor}"
INSTALL_DIR="$HOME/aiosint"
mkdir -p "$INSTALL_DIR/n8n/demo-data/workflows"
mkdir -p "$INSTALL_DIR/venv"

# Copy necessary files if they exist in the current directory (assuming run from repo root)
# If running for the first time from a curl command, these might need to be downloaded.
# For now, we assume this script is running from with the repo or contiguous to the files.

# Ensure we have the latest files
# Using the logic from the original script to download if not present, but preferring local if available.
if [ -f "./n8n/social-api-native.py" ]; then
    cp ./n8n/social-api-native.py "$INSTALL_DIR/n8n/"
else
    # Fallback to download (You might want to update this URL to your repo)
    echo -e "${cColorRojo}[!] social-api-native.py not found locally. Please ensure it is present.${cFinColor}"
fi

if [ -f "./n8n/demo-data/workflows/Agente_Smith.json" ]; then
    cp ./n8n/demo-data/workflows/Agente_Smith.json "$INSTALL_DIR/n8n/demo-data/workflows/"
fi

# 3. Install n8n globally
echo -e "${cColorVerde}[+] Installing n8n globally...${cFinColor}"
sudo npm install -g n8n

# 4. Install Python Tools in Virtual Environment
echo -e "${cColorVerde}[+] Installing Python tools in virtual environment...${cFinColor}"
if [ ! -f "$INSTALL_DIR/venv/bin/activate" ]; then
    python3 -m venv "$INSTALL_DIR/venv"
fi

source "$INSTALL_DIR/venv/bin/activate"

# Upgrade pip
pip install --upgrade pip

# Install Holehe
echo -e "${cColorVerde}  - Installing Holehe...${cFinColor}"
pip install holehe

# Install Maigret
echo -e "${cColorVerde}  - Installing Maigret...${cFinColor}"
pip install maigret

# Install Sherlock
echo -e "${cColorVerde}  - Installing Sherlock...${cFinColor}"
pip install sherlock-project

# Install Flask (for social-api-native.py)
echo -e "${cColorVerde}  - Installing Flask...${cFinColor}"
pip install flask

deactivate

# 5. Fix permissions
echo -e "${cColorVerde}[+] Setting permissions...${cFinColor}"
sudo chown -R $USER:$USER "$INSTALL_DIR"
chmod +x "$INSTALL_DIR/n8n/social-api-native.py"

echo -e "${cColorVerde}[+] Installation complete!${cFinColor}"
echo -e "${cColorVerde}[+] Run './start-native.sh' to start the services.${cFinColor}"
