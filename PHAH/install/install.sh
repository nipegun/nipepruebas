#!/bin/bash

# Definir constantes
  vNomnreRepoGithub='pruebas'
  vUbicArchEnRepo='PHAP'

# Clonar el repo de pruebas
  cd /tmp
  rm -rf /tmp/pruebas/
  git clone https://github.com/nipegun/"$vNombreRepoGithub".git

# Crear carpeta de hacking en la home del usuario
  mkdir -p $HOME/HackingTools/PHAH/

# Mover archivos a la carpeta
  cp -Rv /tmp/"$vNombreRepoGithub"/"$vUbicArchEnRepo"/* $HOME/HackingTools/PHAH/
