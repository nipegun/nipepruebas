#!/bin/bash

# start.sh
# Inicia n8n y la API Social (Python) de forma nativa

cColorRojo='\033[1;31m'
cColorVerde='\033[1;32m'
cFinColor='\033[0m'

INSTALL_DIR="$HOME/aiosint"
VENV_DIR="$INSTALL_DIR/venv"

# Comprobar si existe el entorno virtual
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${cColorRojo}[!] No se encuentra el entorno virtual en $VENV_DIR. Por favor ejecuta install.sh primero.${cFinColor}"
    exit 1
fi

# Cargar variables de entorno si existen
ENV_FILE="$INSTALL_DIR/.env_euskal"
if [ -f "$ENV_FILE" ]; then
    echo -e "${cColorVerde}[+] Cargando variables de entorno desde $ENV_FILE${cFinColor}"
    export $(grep -v '^#' "$ENV_FILE" | xargs)
fi

# Iniciar API Social en segundo plano
echo -e "${cColorVerde}[+] Deteniendo instancias existentes de Social API...${cFinColor}"
pkill -f "social-api.py" || true
# Comprobar proceso en puerto 8000 y matar si existe
PID_8000=$(lsof -t -i:8000)
if [ ! -z "$PID_8000" ]; then
    echo -e "${cColorVerde}[+] Matando proceso $PID_8000 en el puerto 8000...${cFinColor}"
    kill -9 $PID_8000 || true
fi

echo -e "${cColorVerde}[+] Iniciando Social API (segundo plano)...${cFinColor}"
source "$VENV_DIR/bin/activate"
nohup python3 "$INSTALL_DIR/n8n/social-api.py" > "$INSTALL_DIR/social-api.log" 2>&1 &
API_PID=$!
echo -e "    PID: $API_PID"
deactivate

# Iniciar n8n
echo -e "${cColorVerde}[+] Iniciando n8n...${cFinColor}"
# Configuramos variables de entorno para n8n
export N8N_COMMUNITY_PACKAGES_ALLOW_TOOL_USAGE=true
export N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=true
export N8N_RUNNERS_ENABLED=true
export N8N_SECURE_COOKIE=false

n8n start

# Matar API cuando n8n se detenga
kill $API_PID
