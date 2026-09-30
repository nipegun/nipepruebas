#!/usr/bin/env python3
# sudo apt-get -y install python3-requests

import os
import requests
from datetime import datetime

# Nombres de los meses en español
meses_es = [
  "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
  "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

# Crear carpeta para guardar los archivos
os.makedirs("Revistas", exist_ok=True)

# Fecha de inicio y fin
inicio = datetime(2025, 1, 1)
hoy = datetime.today()

# Iterar mes a mes
fecha = inicio
while fecha <= hoy:
  año = fecha.year
  mes_num = f"{fecha.month:02d}"
  mes_nombre = meses_es[fecha.month - 1]

  url = f"https://documentos.campusesine.com/Revistas/ForoEsine/{año}{mes_num}/Actualidad-Inmobiliaria-{mes_nombre}{año}.pdf"
  archivo = f"Revistas/ActualidadInmobiliaria-{año}-{mes_num}-{mes_nombre}.pdf"

  try:
    print(f"Descargando: {url}")
    r = requests.get(url)
    if r.status_code == 200:
      with open(archivo, 'wb') as f:
        f.write(r.content)
      print(f"  Guardado como: {archivo}")
    else:
      print(f"  No encontrada (HTTP {r.status_code})")
  except Exception as e:
    print(f"  Error al descargar: {e}")

  # Avanzar al mes siguiente
  if fecha.month == 12:
    fecha = datetime(fecha.year + 1, 1, 1)
  else:
    fecha = datetime(fecha.year, fecha.month + 1, 1)
