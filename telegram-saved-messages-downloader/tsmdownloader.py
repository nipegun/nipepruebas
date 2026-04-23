#!/usr/bin/env python3

# Pongo a disposición pública este script bajo el término de "software de dominio público".
# Puedes hacer lo que quieras con él porque es libre de verdad; no libre con condiciones como las licencias GNU y otras patrañas similares.
# Si se te llena la boca hablando de libertad entonces hazlo realmente libre.
# No tienes que aceptar ningún tipo de términos de uso o licencia para utilizarlo o modificarlo porque va sin CopyLeft.

# ----------
# Script de NiPeGun para descargar todos los mensajes del chat "Saved messages" de Telegram
#
# Ejecución remota:
#   curl -sL https://raw.githubusercontent.com/nipegun/nipepruebas/refs/heads/main/telegram-saved-messages-downloader/tsmdownloader2.py | python3 - --api-id '12345678' --api-hash 'a1a2a3a4a5a6a7a8a9a0a1a2a3a4a5a6' --phone '+34666666666'
#
# Bajar y editar directamente el archivo en nano:
#   curl -sL https://raw.githubusercontent.com/nipegun/nipepruebas/refs/heads/main/telegram-saved-messages-downloader/tsmdownloader2.py | nano -
# ----------

# ------ Inicio del bloque de instalación de dependencias de paquetes python ------

# Definir los paquetes python que necesita este script siguiendo la convención de diccionario:
# nombre_del_modulo -> nombre_paquete_pip
dPaquetesPython = {
  "telethon": "telethon",
  "rich": "rich"
}

import getpass
import importlib.util
import os
import re
import shutil
import subprocess
import sys

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

cNombreDelPaqueteApt = "python3-pip"

def fPaqueteAptEstaInstalado(pNombreDelPaqueteApt):
  vResultado = subprocess.run(
    ["dpkg", "-s", pNombreDelPaqueteApt],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
  )
  return vResultado.returncode == 0

def fEjecutarComandoElevado(aComando):
  if os.geteuid() == 0:
    subprocess.run(aComando, check=True)
    return

  vRutaSudo = shutil.which("sudo")
  if vRutaSudo:
    subprocess.run([vRutaSudo] + aComando, check=True)
    return

  print("[ERROR] Se necesitan privilegios para instalar dependencias APT y no se encontró sudo.")
  print("[INFO] Ejecuta el script como root o instala previamente python3-pip.")
  sys.exit(1)

def fInstalarPaqueteApt(pNombreDelPaqueteApt):
  print(f"[*] Instalando paquete apt: {pNombreDelPaqueteApt}")
  try:
    fEjecutarComandoElevado(["apt-get", "-y", "update"])
    fEjecutarComandoElevado(["apt-get", "-y", "install", pNombreDelPaqueteApt])
    print(f"[OK] {pNombreDelPaqueteApt} instalado correctamente")
  except subprocess.CalledProcessError as e:
    print(f"[ERROR] Error instalando {pNombreDelPaqueteApt}: {e}")
    sys.exit(1)

def fModuloPythonEstaInstalado(pNombreDelModulo):
  return importlib.util.find_spec(pNombreDelModulo) is not None

def fInstalarPaquetePython(pNombreDelPaquete):
  print(f"[*] Instalando paquete Python: {pNombreDelPaquete}")
  try:
    subprocess.run(
      [sys.executable, "-m", "pip", "install", pNombreDelPaquete, "--break-system-packages"],
      check=True
    )
    print(f"[OK] {pNombreDelPaquete} instalado correctamente")
  except subprocess.CalledProcessError as e:
    print(f"[ERROR] Error instalando {pNombreDelPaquete}: {e}")
    return False

  return True

def fComprobarEInstalarPaquetes(pdPaquetesPython):
  aErrores = []

  for vNombreModulo, vNombrePip in pdPaquetesPython.items():
    if fModuloPythonEstaInstalado(vNombreModulo):
      print(f"[OK] {vNombrePip} ya está instalado")
    else:
      if not fInstalarPaquetePython(vNombrePip):
        aErrores.append(vNombrePip)

  return aErrores

print("=== Comprobando dependencias ===\n")

if not fPaqueteAptEstaInstalado(cNombreDelPaqueteApt):
  fInstalarPaqueteApt(cNombreDelPaqueteApt)
else:
  print(f"[OK] {cNombreDelPaqueteApt} ya está instalado")

print()

aErrores = fComprobarEInstalarPaquetes(dPaquetesPython)

print("\n=== Resumen ===")
if aErrores:
  print(f"[AVISO] Paquetes con errores: {', '.join(aErrores)}")
  sys.exit(1)
else:
  print("[OK] Todas las dependencias instaladas correctamente")

# ------ Fin del bloque de instalación de dependencias ------
# ------ A partir de aquí va el código real del script ------

import argparse
import asyncio

from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn
from rich.progress import Progress
from rich.progress import SpinnerColumn
from rich.progress import TextColumn
from rich.progress import TimeElapsedColumn
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.custom.message import Message

console = Console()

cPatronSoloURL = re.compile(r"^https?://\S+$", re.IGNORECASE)
cPatronCaracteresSeguros = re.compile(r"[^A-Za-z0-9._ -]+")

@dataclass
class Config:
  api_id: int
  api_hash: str
  phone: Optional[str]
  session: str
  output_dir: Path
  code: Optional[str]
  password: Optional[str]
  limit: Optional[int]
  count: bool

def fParsearArgumentos() -> Config:
  vParser = argparse.ArgumentParser(
    description="Descarga todos los mensajes de 'Saved Messages' en archivos locales."
  )
  vParser.add_argument("--api-id", type=int, required=True, help="Telegram API ID")
  vParser.add_argument("--api-hash", required=True, help="Telegram API hash")
  vParser.add_argument("--phone", help="Número de teléfono en formato internacional, ej: +34123456789")
  vParser.add_argument(
    "--session",
    default="tsm_session",
    help="Nombre/ruta base del archivo de sesión de Telethon (default: tsm_session)"
  )
  vParser.add_argument(
    "--output-dir",
    default="messages",
    help="Directorio de salida (default: ./messages)"
  )
  vParser.add_argument("--code", help="Código OTP de Telegram")
  vParser.add_argument("--password", help="Contraseña 2FA")
  vParser.add_argument("--limit", type=int, help="Límite de mensajes a descargar (opcional)")
  vParser.add_argument(
    "-c", "--count",
    action="store_true",
    help="Cuenta todos los mensajes en Saved Messages sin descargarlos"
  )

  vArgs = vParser.parse_args()

  return Config(
    api_id=vArgs.api_id,
    api_hash=vArgs.api_hash,
    phone=vArgs.phone,
    session=vArgs.session,
    output_dir=Path(vArgs.output_dir).expanduser().resolve(),
    code=vArgs.code,
    password=vArgs.password,
    limit=vArgs.limit,
    count=vArgs.count
  )

def fSanitizarNombreDeArchivo(pValor: str, pFallback: str = "archivo") -> str:
  vLimpiado = cPatronCaracteresSeguros.sub("_", pValor).strip(" ._")
  return vLimpiado or pFallback

def fGenerarPrefijoFecha(pFecha: datetime) -> str:
  return f"y{pFecha.year:04d}m{pFecha.month:02d}d{pFecha.day:02d}h{pFecha.hour:02d}m{pFecha.minute:02d}s{pFecha.second:02d}"

def fGenerarPrefijoBase(pMessage: Message) -> str:
  vTimestamp = pMessage.date.astimezone()
  vPrefijoFecha = fGenerarPrefijoFecha(vTimestamp)
  vMessageId = getattr(pMessage, "id", None)

  if vMessageId is None:
    return vPrefijoFecha

  return f"{vPrefijoFecha}-id{vMessageId}"

def fEsSoloURL(pTexto: str) -> bool:
  return bool(cPatronSoloURL.fullmatch(pTexto.strip()))

def fEscribirArchivoDeTexto(pMessage: Message, pPrefijoBase: str, pDirectorioSalida: Path) -> Path:
  vTexto = (pMessage.message or "").strip()
  vExtension = "url" if fEsSoloURL(vTexto) else "txt"
  vRutaArchivo = pDirectorioSalida / f"{pPrefijoBase}-Texto.{vExtension}"
  vRutaArchivo.write_text(vTexto + "\n", encoding="utf-8")
  return vRutaArchivo

def fLeerDesdeTTY(pPrompt: str, pOculto: bool = False) -> str:
  try:
    with open("/dev/tty", "r", encoding="utf-8", errors="ignore") as vTTYIn:
      with open("/dev/tty", "w", encoding="utf-8", errors="ignore") as vTTYOut:
        vTTYOut.write(pPrompt)
        vTTYOut.flush()

        if pOculto:
          return getpass.getpass("", stream=vTTYOut)

        vValor = vTTYIn.readline()
        if vValor == "":
          raise EOFError("No se pudo leer desde /dev/tty")
        return vValor.rstrip("\r\n")
  except Exception:
    if pOculto:
      return getpass.getpass(pPrompt)
    return input(pPrompt)

def fObtenerCodigoOTP(pCfg: Config) -> str:
  if pCfg.code:
    return pCfg.code

  if not sys.stdin.isatty():
    return fLeerDesdeTTY("Introduce el código OTP de Telegram: ")

  return console.input("[bold cyan]Introduce el código OTP de Telegram:[/bold cyan] ")

def fObtenerPassword2FA(pCfg: Config) -> str:
  if pCfg.password:
    return pCfg.password

  if not sys.stdin.isatty():
    return fLeerDesdeTTY("Cuenta con 2FA. Introduce contraseña: ", pOculto=True)

  return console.input(
    "[bold cyan]Cuenta con 2FA. Introduce contraseña:[/bold cyan] ",
    password=True
  )

async def fAsegurarLogin(pClient: TelegramClient, pCfg: Config) -> None:
  if await pClient.is_user_authorized():
    return

  if not pCfg.phone:
    raise RuntimeError(
      "No hay sesión iniciada. Debes pasar --phone para autenticarte la primera vez."
    )

  await pClient.send_code_request(pCfg.phone)
  vCode = fObtenerCodigoOTP(pCfg)

  try:
    await pClient.sign_in(phone=pCfg.phone, code=vCode)
  except SessionPasswordNeededError:
    vPassword = fObtenerPassword2FA(pCfg)
    await pClient.sign_in(password=vPassword)

async def fProcesarMensajes(pClient: TelegramClient, pCfg: Config) -> tuple[int, int, int]:
  pCfg.output_dir.mkdir(parents=True, exist_ok=True)

  vTotalMensajes = 0
  vCantidadMedia = 0
  vCantidadTextos = 0

  with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    TimeElapsedColumn(),
    console=console
  ) as vProgress:
    vTask = vProgress.add_task("Descargando Saved Messages...", total=None)

    async for vMessage in pClient.iter_messages("me", reverse=True, limit=pCfg.limit):
      vTotalMensajes += 1
      vPrefijoBase = fGenerarPrefijoBase(vMessage)

      if vMessage.media:
        vNombreSugerido = "Media"

        if vMessage.file and vMessage.file.name:
          vNombreSugerido = fSanitizarNombreDeArchivo(vMessage.file.name, "Media")

        vNombreDestino = f"{vPrefijoBase}-{vNombreSugerido}"
        vRutaDestino = pCfg.output_dir / vNombreDestino
        vRutaGuardada = await pClient.download_media(vMessage, file=vRutaDestino)

        if vRutaGuardada:
          vCantidadMedia += 1

      if (vMessage.message or "").strip():
        fEscribirArchivoDeTexto(vMessage, vPrefijoBase, pCfg.output_dir)
        vCantidadTextos += 1

      vProgress.update(vTask, description=f"Procesando mensaje #{vTotalMensajes}")
      vProgress.update(vTask, total=vTotalMensajes, completed=vTotalMensajes)

  return vTotalMensajes, vCantidadMedia, vCantidadTextos

async def fContarMensajes(pClient: TelegramClient) -> int:
  vTotalMensajes = 0

  with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    TimeElapsedColumn(),
    console=console
  ) as vProgress:
    vTask = vProgress.add_task("Contando mensajes en Saved Messages...", total=None)

    async for _ in pClient.iter_messages("me"):
      vTotalMensajes += 1
      if vTotalMensajes % 100 == 0:
        vProgress.update(vTask, description=f"Mensajes contados: {vTotalMensajes}")

    vProgress.update(vTask, description=f"Mensajes contados: {vTotalMensajes}")

  return vTotalMensajes

async def fEjecutar(pCfg: Config) -> int:
  console.print(
    Panel.fit(
      "[bold green]Telegram Saved Messages Downloader[/bold green]\n"
      "Exportación cronológica de todo tu chat personal.",
      title="TSMDownloader",
      border_style="cyan"
    )
  )

  vClient = TelegramClient(pCfg.session, pCfg.api_id, pCfg.api_hash)

  vTotal = 0
  vCantidadMedia = 0
  vCantidadTextos = 0

  try:
    await vClient.connect()
    await fAsegurarLogin(vClient, pCfg)
    if pCfg.count:
      vTotal = await fContarMensajes(vClient)
    else:
      vTotal, vCantidadMedia, vCantidadTextos = await fProcesarMensajes(vClient, pCfg)
  finally:
    await vClient.disconnect()

  if pCfg.count:
    console.print(
      Panel.fit(
        f"[bold]Mensajes en Saved Messages:[/bold] {vTotal}",
        title="Conteo",
        border_style="green"
      )
    )
    return 0

  console.print(
    Panel.fit(
      f"[bold]Mensajes procesados:[/bold] {vTotal}\n"
      f"[bold]Archivos multimedia:[/bold] {vCantidadMedia}\n"
      f"[bold]Archivos de texto/url:[/bold] {vCantidadTextos}\n"
      f"[bold]Carpeta de salida:[/bold] {pCfg.output_dir}",
      title="Resumen",
      border_style="green"
    )
  )

  return 0

def main() -> None:
  vCfg = fParsearArgumentos()

  try:
    raise SystemExit(asyncio.run(fEjecutar(vCfg)))
  except KeyboardInterrupt:
    console.print("\n[bold red]Cancelado por el usuario.[/bold red]")
    raise SystemExit(130)

if __name__ == "__main__":
  main()
