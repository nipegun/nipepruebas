# Telegram Saved Messages Eraser

Script de terminal para descargar todos los mensajes del chat **Saved Messages** de Telegram en orden cronológico.

## Ejecución remota directa

```bash
curl -sL https://raw.githubusercontent.com/nipegun/nipepruebas/refs/heads/main/telegram-saved-messages-downloader/tsmdownloader.py | python3 - --api-id '12345678' --api-hash 'a1a2a3a4a5a6a7a8a9a0a1a2a3a4a5a6' --phone '+34666666666'
```

## Cómo conseguir `api-id` y `api-hash`

1. Inicia sesión en https://my.telegram.org con tu número de teléfono.
2. Introduce el código que Telegram te envía (normalmente llega al propio Telegram).
3. En el panel, entra a **API development tools**.
4. Si es la primera vez, completa los campos de creación de app (por ejemplo:
   - **App title**: `tsm-downloader`
   - **Short name**: `tsmdownloader`
   - **Platform**: `Desktop`
   - **Description**: `Descarga de Saved Messages`
5. Guarda el formulario. En la siguiente pantalla verás:
   - **App api_id** → úsalo como valor de `--api-id`
   - **App api_hash** → úsalo como valor de `--api-hash`

> ⚠️ Trata tu `api-hash` como una contraseña: no lo publiques ni lo subas a repositorios.




## Instalación

```bash
python -m venv .venv
source .venv/bin/activate
pip install telethon rich
```

## Uso (una sola línea)

```bash
python3 ./tsmdownloader.py --api-id 123456 --api-hash abcdef123456 --phone +34123456789
```

## Opciones útiles

- `--output-dir /ruta/custom` para cambiar la carpeta destino (por defecto `./messages`).
- `--session mi_sesion` para reutilizar sesión.
- `--code 12345` para pasar OTP por argumento.
- `--password "mi_2fa"` para cuentas con 2FA.
- `--limit 500` para pruebas.

## Formato de nombres

Prefijo de fecha:

- `y2026m03d24h13m58s59-[NombreOriginal]` para media.
- `y2026m03d24h13m58s59-Texto.txt` para texto normal.
- `y2026m03d24h13m58s59-Texto.url` si el mensaje contiene únicamente una URL.
