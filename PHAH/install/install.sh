#!/bin/bash

# ----------
# Script para instalar y configurar PHAH en Debian
#
# Ejecución remota (puede requerir permisos sudo):
#   curl -sL x | bash
#
# Ejecución remota como root (para sistemas sin sudo):
#   curl -sL x | sed 's-sudo--g' | bash
#
# Bajar y editar directamente el archivo en nano
#   curl -sL x | nano -
# ----------

# Definir constantes
  vNombreRepoGithub='pruebas'
  vUbicArchEnRepo='PHAH'

# Definir constantes de color
  cColorAzul='\033[0;34m'
  cColorAzulClaro='\033[1;34m'
  cColorVerde='\033[1;32m'
  cColorRojo='\033[1;31m'
  # Para el color rojo también:
    #echo "$(tput setaf 1)Mensaje en color rojo. $(tput sgr 0)"
  cFinColor='\033[0m'

# Determinar la versión de Debian
  if [ -f /etc/os-release ]; then             # Para systemd y freedesktop.org.
    . /etc/os-release
    cNomSO=$NAME
    cVerSO=$VERSION_ID
  elif type lsb_release >/dev/null 2>&1; then # Para linuxbase.org.
    cNomSO=$(lsb_release -si)
    cVerSO=$(lsb_release -sr)
  elif [ -f /etc/lsb-release ]; then          # Para algunas versiones de Debian sin el comando lsb_release.
    . /etc/lsb-release
    cNomSO=$DISTRIB_ID
    cVerSO=$DISTRIB_RELEASE
  elif [ -f /etc/debian_version ]; then       # Para versiones viejas de Debian.
    cNomSO=Debian
    cVerSO=$(cat /etc/debian_version)
  else                                        # Para el viejo uname (También funciona para BSD).
    cNomSO=$(uname -s)
    cVerSO=$(uname -r)
  fi

# Ejecutar comandos dependiendo de la versión de Debian detectada

  if [ $cVerSO == "13" ]; then

    echo ""
    echo -e "${cColorAzulClaro}  Iniciando el script de instalación de PHAH para Debian 13 (x)...${cFinColor}"
    echo ""

    # Crear el menú
      # Comprobar si el paquete dialog está instalado. Si no lo está, instalarlo.
        if [[ $(dpkg-query -s dialog 2>/dev/null | grep installed) == "" ]]; then
          echo ""
          echo -e "${cColorRojo}  El paquete dialog no está instalado. Iniciando su instalación...${cFinColor}"
          echo ""
          sudo apt-get -y update
          sudo apt-get -y install dialog
          echo ""
        fi
      menu=(dialog --radiolist "Marca las opciones que quieras instalar:" 22 80 16)      # Selección única
        opciones=(
          1 "Instalar en la carpeta del usuario"                            on
          2 "Instalar en un contenedor de systemd (requiere permisos sudo)" off
        )
      choices=$("${menu[@]}" "${opciones[@]}" 2>&1 >/dev/tty)

      for choice in $choices
        do
          case $choice in

            1)

              echo ""
              echo "  Instalando en la carpeta del usuario..."
              echo ""

              # Clonar el repo de pruebas
                cd /tmp
                rm -rf /tmp/"$vNombreRepoGithub"/
                git clone https://github.com/nipegun/"$vNombreRepoGithub".git

              # Crear carpeta de hacking en la home del usuario
                mkdir -p $HOME/HackingTools/PHAH/ 2> /dev/null
                rm -rf $HOME/HackingTools/PHAH/* 2> /dev/null

              # Desactivar posible entorno virtual de python ejecutándose
                deactivate 2> /dev/null

              # Mover archivos a la carpeta
                cp -Rv /tmp/"$vNombreRepoGithub"/"$vUbicArchEnRepo"/* $HOME/HackingTools/PHAH/

              # Crear el entorno virtual de python
                cd $HOME/HackingTools/PHAH/
                python3 -m venv venv

              # Entrar en el entorno virtual e instalar requirements
                source $HOME/HackingTools/PHAH/venv/bin/activate
                pip install -r install/requirements.txt

              # Salir del entorno virtual
                deactivate

              # Notificar fin de la instalación
                echo ""
                echo "  Instalación finalizada."
                echo ""
                echo "  Para ejecutar y posicionarse en la carpeta:"
                echo ""
                echo "    source $HOME/HackingTools/PHAH/venv/bin/activate  && cd $HOME/HackingTools/PHAH/"
                echo ""
                echo ""
                echo "  Para listar servicios:"
                echo ""
                echo "    python phah.py --list-services"
                echo ""
            ;;

            2)

              echo ""
              echo "  Opción 2..."
              echo ""

            ;;

        esac

    done

  elif [ $cVerSO == "12" ]; then

    echo ""
    echo -e "${cColorAzulClaro}  Iniciando el script de instalación de PHAH para Debian 12 (Bookworm)...${cFinColor}"
    echo ""

    echo ""
    echo -e "${cColorRojo}    Comandos para Debian 12 todavía no preparados. Prueba ejecutarlo en otra versión de Debian.${cFinColor}"
    echo ""

  elif [ $cVerSO == "11" ]; then

    echo ""
    echo -e "${cColorAzulClaro}  Iniciando el script de instalación de PHAH para Debian 11 (Bullseye)...${cFinColor}"
    echo ""

    echo ""
    echo -e "${cColorRojo}    Comandos para Debian 11 todavía no preparados. Prueba ejecutarlo en otra versión de Debian.${cFinColor}"
    echo ""

  elif [ $cVerSO == "10" ]; then

    echo ""
    echo -e "${cColorAzulClaro}  Iniciando el script de instalación de PHAH para Debian 10 (Buster)...${cFinColor}"
    echo ""

    echo ""
    echo -e "${cColorRojo}    Comandos para Debian 10 todavía no preparados. Prueba ejecutarlo en otra versión de Debian.${cFinColor}"
    echo ""

  elif [ $cVerSO == "9" ]; then

    echo ""
    echo -e "${cColorAzulClaro}  Iniciando el script de instalación de PHAH para Debian 9 (Stretch)...${cFinColor}"
    echo ""

    echo ""
    echo -e "${cColorRojo}    Comandos para Debian 9 todavía no preparados. Prueba ejecutarlo en otra versión de Debian.${cFinColor}"
    echo ""

  elif [ $cVerSO == "8" ]; then

    echo ""
    echo -e "${cColorAzulClaro}  Iniciando el script de instalación de xxxxxxxxx para Debian 8 (Jessie)...${cFinColor}"
    echo ""

    echo ""
    echo -e "${cColorRojo}    Comandos para Debian 8 todavía no preparados. Prueba ejecutarlo en otra versión de Debian.${cFinColor}"
    echo ""

  elif [ $cVerSO == "7" ]; then

    echo ""
    echo -e "${cColorAzulClaro}  Iniciando el script de instalación de xxxxxxxxx para Debian 7 (Wheezy)...${cFinColor}"
    echo ""

    echo ""
    echo -e "${cColorRojo}    Comandos para Debian 7 todavía no preparados. Prueba ejecutarlo en otra versión de Debian.${cFinColor}"
    echo ""

  fi
