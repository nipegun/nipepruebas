#!/usr/bin/env -S PYTHONDONTWRITEBYTECODE=1 python3

# Pongo a disposición pública este script bajo el término de "software de dominio público".
# Puedes hacer lo que quieras con él porque es libre de verdad; no libre con condiciones como las licencias GNU y otras patrañas similares.
# Si se te llena la boca hablando de libertad entonces hazlo realmente libre.
# No tienes que aceptar ningún tipo de términos de uso o licencia para utilizarlo o modificarlo porque va sin CopyLeft.

# ----------
# Script de NiPeGun para descargar todos los mensajes del chat "Saved messages" de Telegram
#
# Ejecución remota (puede requerir permisos sudo):
#   curl -sL https://raw.githubusercontent.com/nipegun/nipepruebas/refs/heads/main/telegram-saved-messages-downloader/tsmdownloader.py | python3 - --api-id 'x' --api-hash 'x' --phone '+34666666666'
#
# Bajar y editar directamente el archivo en nano
#   curl -sL https://raw.githubusercontent.com/nipegun/nipepruebas/refs/heads/main/telegram-saved-messages-downloader/tsmdownloader.py | nano -
# ----------

# ------ Inicio del bloque de instalación de dependencias de paquetes python ------

# Definir los paquetes python que necesita este script siguiendo la convención de ciccionario: nombre_del_modulo -> nombre_paquete_pip (para casos donde difieren)
dPaquetesPython = {
  "teleton": "teleton",
  "rich": "rich"
}

import importlib.util
import subprocess
import sys

cNombreDelPaqueteApt = "python3-pip"

def fPaqueteAptEstaInstalado(pNombreDelPaqueteApt):
  """Verifica si un paquete apt está instalado."""
  vResultado = subprocess.run(
    ["dpkg", "-s", pNombreDelPaqueteApt],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
  )
  return vResultado.returncode == 0

def fInstalarPaqueteApt(pNombreDelPaqueteApt):
  """Instala un paquete mediante apt."""
  print(f"[*] Instalando paquete apt: {pNombreDelPaqueteApt}")
  try:
    subprocess.run(
      ["sudo", "apt-get", "-y", "update"],
      check=True
    )
    subprocess.run(
      ["sudo", "apt-get", "-y", "install", pNombreDelPaqueteApt],
      check=True
    )
    print(f"[✓] {pNombreDelPaqueteApt} instalado correctamente")
  except subprocess.CalledProcessError as e:
    print(f"[✗] Error instalando {pNombreDelPaqueteApt}: {e}")
    sys.exit(1)

def fModuloPythonEstaInstalado(pNombreDelModulo):
  """Verifica si un módulo Python está disponible."""
  return importlib.util.find_spec(pNombreDelModulo) is not None

def fInstalarPaquetePython(pNombreDelPaquete):
  """Instala un paquete Python mediante pip."""
  print(f"[*] Instalando paquete Python: {pNombreDelPaquete}")
  try:
    subprocess.run(
      [
        sys.executable,
        "-m", "pip", "install",
        pNombreDelPaquete,
        "--break-system-packages"
      ],
      check=True
    )
    print(f"[✓] {pNombreDelPaquete} instalado correctamente")
  except subprocess.CalledProcessError as e:
    print(f"[✗] Error instalando {pNombreDelPaquete}: {e}")
    return False
  return True

def fComprobarEInstalarPaquetes(pdPaquetesPython):
  """Comprueba e instala los paquetes Python necesarios."""
  aErrores = []
  for vNombreModulo, vNombrePip in pdPaquetesPython.items():
    if fModuloPythonEstaInstalado(vNombreModulo):
      print(f"[✓] {vNombrePip} ya está instalado")
    else:
      if not fInstalarPaquetePython(vNombrePip):
        aErrores.append(vNombrePip)
  return aErrores

print("=== Comprobando dependencias ===\n")

if not fPaqueteAptEstaInstalado(cNombreDelPaqueteApt):
  fInstalarPaqueteApt(cNombreDelPaqueteApt)
else:
  print(f"[✓] {cNombreDelPaqueteApt} ya está instalado")

print()

aErrores = fComprobarEInstalarPaquetes(dPaquetesPython)

print("\n=== Resumen ===")
if aErrores:
  print(f"[!] Paquetes con errores: {', '.join(aErrores)}")
  sys.exit(1)
else:
  print("[✓] Todas las dependencias instaladas correctamente")

# ------ Fin del bloque de instalación de dependencias. A partir de aquí va el código real del script ------

from __future__ import annotations

import argparse
import asyncio
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.custom.message import Message

from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

console = Console()
URL_ONLY_PATTERN = re.compile(r"^https?://\S+$", re.IGNORECASE)
SAFE_CHARS_PATTERN = re.compile(r"[^A-Za-z0-9._ -]+")


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


def parse_args() -> Config:
    parser = argparse.ArgumentParser(
        description="Descarga todos los mensajes de 'Saved Messages' en archivos locales."
    )
    parser.add_argument("--api-id", type=int, required=True, help="Telegram API ID")
    parser.add_argument("--api-hash", required=True, help="Telegram API hash")
    parser.add_argument("--phone", help="Número de teléfono en formato internacional, ej: +34123456789")
    parser.add_argument(
        "--session",
        default="tsm_session",
        help="Nombre/ruta base del archivo de sesión de Telethon (default: tsm_session)",
    )
    parser.add_argument(
        "--output-dir",
        default="messages",
        help="Directorio de salida (default: ./messages)",
    )
    parser.add_argument("--code", help="Código OTP de Telegram (si no se pasa, se pedirá en terminal)")
    parser.add_argument("--password", help="Contraseña 2FA (si aplica)")
    parser.add_argument("--limit", type=int, help="Límite de mensajes a descargar (opcional)")

    args = parser.parse_args()
    return Config(
        api_id=args.api_id,
        api_hash=args.api_hash,
        phone=args.phone,
        session=args.session,
        output_dir=Path(args.output_dir).expanduser().resolve(),
        code=args.code,
        password=args.password,
        limit=args.limit,
    )


def sanitize_filename(value: str, fallback: str = "archivo") -> str:
    cleaned = SAFE_CHARS_PATTERN.sub("_", value).strip(" ._")
    return cleaned or fallback


def date_prefix(dt: datetime) -> str:
    return f"y{dt.year:04d}m{dt.month:02d}d{dt.day:02d}h{dt.hour:02d}m{dt.minute:02d}s{dt.second:02d}"


def is_url_only(text: str) -> bool:
    return bool(URL_ONLY_PATTERN.fullmatch(text.strip()))


def write_text_file(message: Message, base_prefix: str, output_dir: Path) -> Path:
    text = (message.message or "").strip()
    extension = "url" if is_url_only(text) else "txt"
    file_path = output_dir / f"{base_prefix}-Texto.{extension}"
    file_path.write_text(text + "\n", encoding="utf-8")
    return file_path


async def ensure_login(client: TelegramClient, cfg: Config) -> None:
    if await client.is_user_authorized():
        return

    if not cfg.phone:
        raise RuntimeError(
            "No hay sesión iniciada. Debes pasar --phone para autenticarte la primera vez."
        )

    await client.send_code_request(cfg.phone)
    code = cfg.code or console.input("[bold cyan]Introduce el código OTP de Telegram:[/bold cyan] ")

    try:
        await client.sign_in(phone=cfg.phone, code=code)
    except SessionPasswordNeededError:
        password = cfg.password or console.input(
            "[bold cyan]Cuenta con 2FA. Introduce contraseña:[/bold cyan] ", password=True
        )
        await client.sign_in(password=password)


async def process_messages(client: TelegramClient, cfg: Config) -> tuple[int, int, int]:
    cfg.output_dir.mkdir(parents=True, exist_ok=True)
    total_messages = 0
    media_saved = 0
    text_saved = 0

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Descargando Saved Messages...", total=None)

        async for message in client.iter_messages("me", reverse=True, limit=cfg.limit):
            total_messages += 1
            timestamp = message.date.astimezone()
            prefix = date_prefix(timestamp)

            if message.media:
                guessed_name = "Media"
                if message.file and message.file.name:
                    guessed_name = sanitize_filename(message.file.name, "Media")
                target_name = f"{prefix}-{guessed_name}"
                target_path = cfg.output_dir / target_name
                saved_path = await client.download_media(message, file=target_path)

                if saved_path:
                    media_saved += 1

            if (message.message or "").strip():
                write_text_file(message, prefix, cfg.output_dir)
                text_saved += 1

            progress.update(task, description=f"Procesando mensaje #{total_messages}")

        progress.update(task, total=total_messages, completed=total_messages)

    return total_messages, media_saved, text_saved


async def run(cfg: Config) -> int:
    console.print(
        Panel.fit(
            "[bold green]Telegram Saved Messages Downloader[/bold green]\n"
            "Exportación cronológica de todo tu chat personal.",
            title="TSMDownloader",
            border_style="cyan",
        )
    )

    client = TelegramClient(cfg.session, cfg.api_id, cfg.api_hash)

    async with client:
        await ensure_login(client, cfg)
        total, media_count, text_count = await process_messages(client, cfg)

    console.print(
        Panel.fit(
            f"[bold]Mensajes procesados:[/bold] {total}\n"
            f"[bold]Archivos multimedia:[/bold] {media_count}\n"
            f"[bold]Archivos de texto/url:[/bold] {text_count}\n"
            f"[bold]Carpeta de salida:[/bold] {cfg.output_dir}",
            title="Resumen",
            border_style="green",
        )
    )
    return 0


def main() -> None:
    cfg = parse_args()
    try:
        raise SystemExit(asyncio.run(run(cfg)))
    except KeyboardInterrupt:
        console.print("\n[bold red]Cancelado por el usuario.[/bold red]")
        raise SystemExit(130)


if __name__ == "__main__":
    main()
