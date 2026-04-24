#!/usr/bin/env python3

# Pongo a disposición pública este script bajo el término de "software de dominio público".
# Puedes hacer lo que quieras con él porque es libre de verdad; no libre con condiciones como las licencias GNU y otras patrañas similares.
# Si se te llena la boca hablando de libertad entonces hazlo realmente libre.
# No tienes que aceptar ningún tipo de términos de uso o licencia para utilizarlo o modificarlo porque va sin CopyLeft.

# ----------
# Script de NiPeGun para borrar todos los mensajes del chat "Saved messages" de Telegram
#
# Ejecución remota:
#   curl -sL https://raw.githubusercontent.com/nipegun/nipepruebas/refs/heads/main/telegram-saved-messages-eraser/tsmeraser.py | python3 - --api-id '12345678' --api-hash 'a1a2a3a4a5a6a7a8a9a0a1a2a3a4a5a6' --phone '+34666666666'
#
# Bajar y editar directamente el archivo en nano:
#   curl -sL https://raw.githubusercontent.com/nipegun/nipepruebas/refs/heads/main/telegram-saved-messages-eraser/tsmeraser.py | nano -
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
import shutil
import subprocess
import sys

from dataclasses import dataclass
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

console = Console()

@dataclass
class Config:
  api_id: int
  api_hash: str
  phone: Optional[str]
  session: str
  code: Optional[str]
  password: Optional[str]
  limit: Optional[int]

def fParsearArgumentos() -> Config:
  vParser = argparse.ArgumentParser(
    description="Borra todos los mensajes de 'Saved Messages'."
  )
  vParser.add_argument("--api-id", type=int, required=True, help="Telegram API ID")
  vParser.add_argument("--api-hash", required=True, help="Telegram API hash")
  vParser.add_argument("--phone", help="Número de teléfono en formato internacional, ej: +34123456789")
  vParser.add_argument(
    "--session",
    default="tsm_session",
    help="Nombre/ruta base del archivo de sesión de Telethon (default: tsm_session)"
  )
  vParser.add_argument("--code", help="Código OTP de Telegram")
  vParser.add_argument("--password", help="Contraseña 2FA")
  vParser.add_argument("--limit", type=int, help="Límite de mensajes a borrar (opcional)")

  vArgs = vParser.parse_args()

  return Config(
    api_id=vArgs.api_id,
    api_hash=vArgs.api_hash,
    phone=vArgs.phone,
    session=vArgs.session,
    code=vArgs.code,
    password=vArgs.password,
    limit=vArgs.limit
  )

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

async def fBorrarMensajes(pClient: TelegramClient, pCfg: Config, pTotalMensajes: int) -> int:
  vContadorBorrados = 0
  vIdsLote = []

  with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    TimeElapsedColumn(),
    console=console
  ) as vProgress:
    vTask = vProgress.add_task("Borrando Saved Messages...", total=pTotalMensajes)

    async for vMessage in pClient.iter_messages("me", reverse=True, limit=pCfg.limit):
      vIdsLote.append(vMessage.id)

      if len(vIdsLote) >= 100:
        await pClient.delete_messages("me", vIdsLote)
        vContadorBorrados += len(vIdsLote)
        vIdsLote = []
        vProgress.update(
          vTask,
          description=f"Borrados {vContadorBorrados} de {pTotalMensajes}",
          completed=vContadorBorrados
        )

    if vIdsLote:
      await pClient.delete_messages("me", vIdsLote)
      vContadorBorrados += len(vIdsLote)
      vProgress.update(
        vTask,
        description=f"Borrados {vContadorBorrados} de {pTotalMensajes}",
        completed=vContadorBorrados
      )

  return vContadorBorrados

async def fContarMensajes(pClient: TelegramClient) -> int:
  vResultado = await pClient.get_messages("me", limit=0)
  vTotal = getattr(vResultado, "total", None)

  if vTotal is None:
    vResultado = await pClient.get_messages("me", limit=1)
    vTotal = getattr(vResultado, "total", 0) or 0

  return vTotal

async def fEjecutar(pCfg: Config) -> int:
  console.print(
    Panel.fit(
      "[bold green]Telegram Saved Messages Eraser[/bold green]\n"
      "Borrado masivo de todo tu chat personal.",
      title="TSMEraser",
      border_style="cyan"
    )
  )

  vClient = TelegramClient(pCfg.session, pCfg.api_id, pCfg.api_hash)
  vTotalBorrados = 0

  try:
    await vClient.connect()
    await fAsegurarLogin(vClient, pCfg)

    console.print("[cyan]Contando mensajes en Saved Messages...[/cyan]")
    vTotalMensajes = await fContarMensajes(vClient)
    console.print(f"[cyan]Total de mensajes en Saved Messages: [bold]{vTotalMensajes}[/bold][/cyan]\n")

    vTotalABorrar = vTotalMensajes
    if pCfg.limit is not None and pCfg.limit < vTotalMensajes:
      vTotalABorrar = pCfg.limit
      console.print(f"[yellow]Se borrarán solo {vTotalABorrar} mensajes (límite aplicado).[/yellow]\n")

    if vTotalABorrar == 0:
      console.print("[green]No hay mensajes para borrar.[/green]")
      return 0

    vTotalBorrados = await fBorrarMensajes(vClient, pCfg, vTotalABorrar)
  finally:
    await vClient.disconnect()

  console.print(
    Panel.fit(
      f"[bold]Mensajes borrados:[/bold] {vTotalBorrados}",
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
