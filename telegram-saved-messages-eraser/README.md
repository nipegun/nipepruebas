# Telegram Saved Messages Eraser

Script de terminal para **borrar todos los mensajes** del chat **Saved Messages** de Telegram.

## Ejecución remota directa

```bash
curl -sL https://raw.githubusercontent.com/nipegun/nipepruebas/refs/heads/main/telegram-saved-messages-eraser/tsmeraser.py | python3 - --api-id '12345678' --api-hash 'a1a2a3a4a5a6a7a8a9a0a1a2a3a4a5a6' --phone '+34666666666'
```

## Cómo conseguir `api-id` y `api-hash`

1. Inicia sesión en https://my.telegram.org con tu número de teléfono.
2. Introduce el código que Telegram te envía (normalmente llega al propio Telegram).
3. En el panel, entra a **API development tools**.
4. Si es la primera vez, completa los campos de creación de app (por ejemplo:
   - **App title**: `tsm-eraser`
   - **Short name**: `tsmeraser`
   - **Platform**: `Desktop`
   - **Description**: `Borrado de Saved Messages`
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
python3 ./tsmeraser.py --api-id 123456 --api-hash abcdef123456 --phone +34123456789
```

## Opciones útiles

- `--session mi_sesion` para reutilizar sesión.
- `--code 12345` para pasar OTP por argumento.
- `--password "mi_2fa"` para cuentas con 2FA.
- `--limit 500` para borrar solo una cantidad concreta (útil para pruebas).

## Qué hace exactamente

- Cuenta cuántos mensajes hay en `Saved Messages`.
- Los borra por lotes hasta vaciar el chat (o hasta el límite indicado).
- Muestra una barra de progreso y un resumen final.

## Aviso

Este proceso elimina mensajes de forma irreversible en tu cuenta. Úsalo bajo tu responsabilidad.
