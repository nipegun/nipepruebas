# Telegram Saved Messages Downloader

Script de terminal para descargar todos los mensajes del chat **Saved Messages** de Telegram en orden cronológico.

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate
pip install telethon rich
```

## Uso (una sola línea)

```bash
python tsmdownloader.py --api-id 123456 --api-hash abcdef123456 --phone +34123456789
```

## Opciones útiles

- `--output-dir /ruta/custom` para cambiar la carpeta destino (por defecto `./messages`).
- `--session mi_sesion` para reutilizar sesión.
- `--code 12345` para pasar OTP por argumento.
- `--password "mi_2fa"` para cuentas con 2FA.
- `--limit 500` para pruebas.
- `--utc` para generar prefijos con fecha UTC.
- `--no-metadata-csv` para desactivar `messages_index.csv`.

## Formato de nombres

Prefijo de fecha:

- `y2026m03d24h13m58s59-[NombreOriginal]` para media.
- `y2026m03d24h13m58s59-Texto.txt` para texto normal.
- `y2026m03d24h13m58s59-Texto.url` si el mensaje contiene únicamente una URL.

Si hay colisiones de nombre (por ejemplo, varios mensajes en el mismo segundo), se añade sufijo `__1`, `__2`, etc. para no sobrescribir archivos.

## Archivo índice

Por defecto, se crea `messages_index.csv` con columnas:

- `message_id`
- `telegram_date`
- `type` (`media`, `text`, `url_text`)
- `saved_file`
