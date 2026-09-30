#!/usr/bin/env python3
# sudo apt-get -y install python3-requests

import os
import requests
from datetime import datetime

# Array con los nombres de los meses en español
aMeses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

# Crear carpeta de salida si no existe
os.makedirs("Revistas", exist_ok=True)

# Constantes de fecha de inicio
cAnioInicio = 2008
cMesInicio = 1

# Variables de fechas
vFechaInicio = datetime(cAnioInicio, cMesInicio, 1)
vFechaHoy = datetime.today()

# Inicializar iterador
vFecha = vFechaInicio

while vFecha <= vFechaHoy:
  vAnio = vFecha.year
  vMes = vFecha.month
  vMesConCero = f"{vMes:02d}"
  vNombreMes = aMeses[vMes - 1]

  vURL = f"https://documentos.campusesine.com/Revistas/ForoEsine/{vAnio}{vMesConCero}/{vAnio}{vNombreMes}.pdf"
  vRutaDestino = f"Revistas/RevistaForoESINE-a{vAnio}m{vMesConCero}.pdf"

  try:
    print(f"Descargando: {vURL}")
    vRespuesta = requests.get(vURL)
    if vRespuesta.status_code == 200:
      with open(vRutaDestino, 'wb') as vArchivo:
        vArchivo.write(vRespuesta.content)
      print(f"  Guardado como: {vRutaDestino}")
    else:
      print(f"  No encontrada (HTTP {vRespuesta.status_code})")
  except Exception as vError:
    print(f"  Error al descargar: {vError}")

  # Avanzar al siguiente mes
  if vMes == 12:
    vFecha = datetime(vAnio + 1, 1, 1)
  else:
    vFecha = datetime(vAnio, vMes + 1, 1)
