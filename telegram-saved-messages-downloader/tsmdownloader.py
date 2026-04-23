#!/usr/bin/env python3
"""Telegram Saved Messages Downloader (terminal-first)."""

from __future__ import annotations

import argparse
import asyncio
import csv
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from telethon import TelegramClient
from telethon.errors import RPCError, SessionPasswordNeededError
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
    utc: bool
    metadata_csv: bool


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
    parser.add_argument(
        "--utc",
        action="store_true",
        help="Usar UTC para el prefijo de fecha (por defecto: hora local)",
    )
    parser.add_argument(
        "--no-metadata-csv",
        action="store_true",
        help="No generar messages_index.csv con trazabilidad de exportación.",
    )

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
        utc=args.utc,
        metadata_csv=not args.no_metadata_csv,
    )


def sanitize_filename(value: str, fallback: str = "archivo") -> str:
    cleaned = SAFE_CHARS_PATTERN.sub("_", value).strip(" ._")
    return cleaned or fallback


def date_prefix(dt: datetime) -> str:
    return f"y{dt.year:04d}m{dt.month:02d}d{dt.day:02d}h{dt.hour:02d}m{dt.minute:02d}s{dt.second:02d}"


def is_url_only(text: str) -> bool:
    return bool(URL_ONLY_PATTERN.fullmatch(text.strip()))


def ensure_unique_path(path: Path) -> Path:
    if not path.exists():
        return path

    stem = path.stem
    suffix = path.suffix
    counter = 1
    while True:
        candidate = path.with_name(f"{stem}__{counter}{suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def write_text_file(message: Message, base_prefix: str, output_dir: Path) -> Path:
    text = (message.message or "").strip()
    extension = "url" if is_url_only(text) else "txt"
    file_path = ensure_unique_path(output_dir / f"{base_prefix}-Texto.{extension}")
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
    metadata_rows: list[list[str]] = []

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
            timestamp = message.date.astimezone(timezone.utc) if cfg.utc else message.date.astimezone()

            prefix = date_prefix(timestamp)

            if message.media:
                guessed_name = "Media"
                if message.file and message.file.name:
                    guessed_name = sanitize_filename(message.file.name, "Media")
                target_name = f"{prefix}-{guessed_name}"
                target_path = ensure_unique_path(cfg.output_dir / target_name)
                saved_path = await client.download_media(message, file=target_path)

                if saved_path:
                    media_saved += 1
                    metadata_rows.append([
                        str(message.id),
                        str(message.date),
                        "media",
                        Path(saved_path).name,
                    ])

            if (message.message or "").strip():
                text_file = write_text_file(message, prefix, cfg.output_dir)
                text_saved += 1
                metadata_rows.append([
                    str(message.id),
                    str(message.date),
                    "url_text" if is_url_only(message.message or "") else "text",
                    text_file.name,
                ])

            progress.update(task, description=f"Procesando mensaje #{total_messages}")

        progress.update(task, total=total_messages, completed=total_messages)

    if cfg.metadata_csv and metadata_rows:
        index_file = cfg.output_dir / "messages_index.csv"
        with index_file.open("w", encoding="utf-8", newline="") as fh:
            writer = csv.writer(fh)
            writer.writerow(["message_id", "telegram_date", "type", "saved_file"])
            writer.writerows(metadata_rows)

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
    except (RuntimeError, RPCError) as exc:
        console.print(f"[bold red]Error:[/bold red] {exc}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
