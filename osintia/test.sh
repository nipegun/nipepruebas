#!/bin/bash

# Comprobar si el paquete curl está instalado. Si no lo está, instalarlo.
  if [[ $(dpkg-query -s curl 2>/dev/null | grep installed) == "" ]]; then
    echo ""
    echo -e "${cColorRojo}  El paquete curl no está instalado. Iniciando su instalación...${cFinColor}"
    echo ""
    sudo apt-get -y update
    sudo apt-get -y install curl
    echo ""
  fi

# Comprobar si el paquete jq está instalado. Si no lo está, instalarlo.
  if [[ $(dpkg-query -s jq 2>/dev/null | grep installed) == "" ]]; then
    echo ""
    echo -e "${cColorRojo}  El paquete jq no está instalado. Iniciando su instalación...${cFinColor}"
    echo ""
    sudo apt-get -y update
    sudo apt-get -y install jq
    echo ""
  fi

curl -X POST http://localhost:8000/scrape \
-H "Content-Type: application/json" \
-d '{
    "url": "https://boardmix.com/",
    "prompt": "Extrae la información de marca que se detalla a continuación. Campos a extraer (usa `null` si no se detecta): (company_name, domain, primary_color, background_color, text_color, button_color, button_text_color, font_family, brand_claim, short_description, industry, country, services_products, key_clients, communication_tone, writing_style, market_positioning)"
}' | jq
