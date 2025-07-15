#!/bin/bash

# Comprobar si el paquete docker-ce está instalado. Si no lo está, instalarlo.
  if [[ $(dpkg-query -s docker-ce 2>/dev/null | grep installed) == "" ]]; then
    echo ""
    echo -e "${cColorRojo}  El paquete docker-ce no está instalado. Iniciando su instalación...${cFinColor}"
    echo ""
    curl -sL https://raw.githubusercontent.com/nipegun/d-scripts/master/SoftInst/ParaCLI/DockerCE-Instalar.sh | bash
    echo ""
  fi

# Comprobar si el paquete docker-compose está instalado. Si no lo está, instalarlo.
  if [[ $(dpkg-query -s docker-compose 2>/dev/null | grep installed) == "" ]]; then
    echo ""
    echo -e "${cColorRojo}  El paquete docker-compose no está instalado. Iniciando su instalación...${cFinColor}"
    echo ""
    sudo apt-get -y install docker-compose
    echo ""
  fi

docker-compose up --build --remove-orphans -d
docker exec -it n8n /usr/bin/python3.12 /opt/social-api.py
