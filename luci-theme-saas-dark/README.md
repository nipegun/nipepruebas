# luci-theme-saas-dark

Theme oscuro estilo SaaS moderno para LuCI (OpenWrt). Paleta basada en azules muy oscuros con acentos de gradiente púrpura→azul, sidebar fija con menú dinámico y cards con glassmorphism sutil.

El repositorio contiene **dos variantes** del theme, una para cada línea de OpenWrt:

| Variante | Compatibilidad | Gestor de paquetes | Subcarpeta |
| --- | --- | --- | --- |
| **legacy** | OpenWrt `19.07.x` – `24.10.x` | `opkg` | [`legacy/`](legacy/) |
| **modern** | OpenWrt `25.12.x` y superiores | `apk` | [`modern/`](modern/) |

Ambas variantes comparten el mismo diseño visual y los mismos assets (CSS/JS), pero difieren en la forma de construir el paquete y en los detalles de compatibilidad del dispatcher de LuCI.

## Estructura común de ambas variantes

```
<variante>/
├── Makefile                                        (meta del paquete LuCI)
├── install.sh                                      (instalación desde clon local)
├── install-curl.sh                                 (instalación directa en router vía curl)
├── htdocs/
│   └── luci-static/
│       ├── resources/menu-saas-dark.js             (módulo JS del menú dinámico)
│       └── saas-dark/
│           ├── css/style.css                       (theme completo)
│           └── js/theme.js                         (toggles de sidebar, overlay, etc.)
├── luasrc/
│   └── view/themes/saas-dark/
│       ├── header.htm                              (shell de página + sidebar)
│       ├── footer.htm                              (cierre + carga del módulo de menú)
│       └── sysauth.htm                             (pantalla de login)
└── root/
    └── etc/uci-defaults/99-theme-saas-dark         (UCI defaults del theme)
```

## Cómo funciona la navegación

LuCI construye el menú en el cliente (vía JavaScript), no en el servidor. El footer invoca:

```html
<script>L.require('menu-saas-dark')</script>
```

Ese módulo (`/www/luci-static/resources/menu-saas-dark.js`) usa `ui.menu.load()` para obtener el árbol de menú dinámico y lo renderiza en el `#topmenu` de la sidebar y en `#tabmenu` del área principal.

## Directivas de diseño gráfico

- Fondo azul muy oscuro (`#060d1a`, `#0d1627`).
- Cards con glassmorphism sutil, borde tenue y `border-radius` ≥ 12 px.
- Acentos en gradiente púrpura→azul (`#7c3aed` → `#2563eb`) sobre CTAs y focus.
- Sidebar fija (260 px), header superior (56 px) y área principal con scroll independiente.
- Hover y microtransiciones suaves (`transition: … 0.15s ease`).
- Se evita Bootstrap como base y los grises planos sin matiz.

## Paleta de referencia (CSS variables)

```css
:root {
  --bg-base:        #060d1a;
  --bg-surface:     #0d1627;
  --bg-elevated:    #111d30;
  --border-subtle:  rgba(255, 255, 255, 0.07);
  --accent-primary: #7c3aed;
  --accent-blue:    #2563eb;
  --accent-cyan:    #06b6d4;
  --text-primary:   #f1f5f9;
  --text-secondary: rgba(241, 245, 249, 0.45);
  --success:        #10b981;
  --danger:         #ef4444;
  --warning:        #f59e0b;
  --gradient-main:  linear-gradient(135deg, #7c3aed, #2563eb);
  --shadow-lg:      0 20px 40px rgba(0, 0, 0, 0.45);
  --radius-lg:      14px;
}
```

## Instalación rápida

### Variante legacy (OpenWrt ≤ 24.10.x, `opkg`)

```sh
curl -fsSL https://raw.githubusercontent.com/nipegun/nipepruebas/main/luci-theme-saas-dark/legacy/install-curl.sh | sh
```

### Variante modern (OpenWrt ≥ 25.12.x, `apk`)

```sh
curl -fsSL https://raw.githubusercontent.com/nipegun/nipepruebas/main/luci-theme-saas-dark/modern/install-curl.sh | sh
```

Los detalles (clonado local, Buildroot, activación manual del theme) están en el README de cada variante.
