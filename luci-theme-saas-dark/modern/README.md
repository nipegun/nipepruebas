# luci-theme-saas-dark (modern)

Variante **modern** del theme `luci-theme-saas-dark`, orientada a OpenWrt `25.12.x` y superiores, donde LuCI ya corre sobre el dispatcher ucode moderno y la instalación de paquetes en router se realiza con **apk** (no con opkg).

## Compatibilidad

- OpenWrt `25.12.x` y superiores.
- Dispatcher ucode moderno (no requiere `luci-compat`).
- Buildroot oficial de OpenWrt para compilar el paquete LuCI.
- Instalación en router con `apk add` sobre paquetes `.apk` o con los scripts `install.sh` / `install-curl.sh`.

## Estructura de archivos

```
modern/
├── Makefile
├── install.sh                                  (instalación desde clon local)
├── install-curl.sh                             (instalación directa en router)
├── htdocs/
│   └── luci-static/
│       ├── resources/menu-saas-dark.js         (módulo JS que construye el menú dinámico)
│       └── saas-dark/
│           ├── css/style.css                   (~1750 líneas, theme completo)
│           └── js/theme.js                     (toggles de sidebar, overlay, ESC, etc.)
├── luasrc/
│   └── view/themes/saas-dark/
│       ├── header.htm                          (shell, sidebar y contenedores que LuCI espera)
│       ├── footer.htm                          (carga theme.js y dispara L.require('menu-saas-dark'))
│       └── sysauth.htm                         (pantalla de login con card SaaS)
└── root/
    └── etc/uci-defaults/99-theme-saas-dark     (UCI defaults)
```

### Notas de compatibilidad modern

- Templates y footer operan sobre el dispatcher ucode 25.12+, con acceso directo al árbol de menú sin el puente `luci-compat`.
- Los contenedores DOM que LuCI requiere (`#topmenu`, `#tabmenu`, `#modemenu`, `#maincontent`, `#indicators`) están presentes en el header/footer con `display:none` inicial.
- Las estadísticas del footer se leen directamente de `/proc/uptime`, `/proc/loadavg` y `/proc/meminfo` para evitar incompatibilidades con diferentes versiones de BusyBox.

## Instalación rápida (curl)

```sh
curl -fsSL https://raw.githubusercontent.com/nipegun/nipepruebas/main/luci-theme-saas-dark/modern/install-curl.sh | sh
```

El script `install-curl.sh`:

1. Comprueba que `curl` está disponible y que el sistema es OpenWrt.
2. Descarga los templates, CSS, JS, módulo de menú y UCI defaults a sus rutas finales.
3. Aplica `uci set luci.main.mediaurlbase='/luci-static/saas-dark'` y reinicia `uhttpd`.

## Instalación desde clon local

```sh
git clone https://github.com/nipegun/nipepruebas.git
cd nipepruebas/luci-theme-saas-dark/modern
sh install.sh
uci set luci.main.mediaurlbase='/luci-static/saas-dark'
uci commit luci
/etc/init.d/uhttpd restart
```

`install.sh` copia los mismos archivos que `install-curl.sh` pero desde el clon local (sin conexión a internet).

## Instalación en entorno de desarrollo (Buildroot)

1. Copia la carpeta dentro de `feeds/luci/themes/` o en `package/` dentro del árbol de OpenWrt.
2. Actualiza feeds e instala el paquete:

```sh
./scripts/feeds update luci
./scripts/feeds install luci-theme-saas-dark
make menuconfig  # LuCI -> Themes -> luci-theme-saas-dark
```

3. Compila el paquete:

```sh
make package/luci-theme-saas-dark/{clean,compile} V=sc
```

4. Copia el paquete `.apk` al router:

```sh
scp bin/packages/*/luci/luci-theme-saas-dark_*.apk root@192.168.1.1:/tmp
```

5. Instala con `apk`:

```sh
ssh root@192.168.1.1 "apk add --allow-untrusted /tmp/luci-theme-saas-dark_*.apk"
```

6. Activa el theme:

```sh
uci set luci.main.mediaurlbase='/luci-static/saas-dark'
uci commit luci
/etc/init.d/uhttpd restart
```

## Instalación directa en router (sin Buildroot)

```sh
ssh root@192.168.1.1
cd /tmp
wget https://tu-servidor/paquetes/luci-theme-saas-dark_2.0.0_all.apk
apk add --allow-untrusted /tmp/luci-theme-saas-dark_2.0.0_all.apk
uci set luci.main.mediaurlbase='/luci-static/saas-dark'
uci commit luci
/etc/init.d/uhttpd restart
```

## Activación manual (tras instalar)

```sh
uci set luci.main.mediaurlbase='/luci-static/saas-dark'
uci commit luci
/etc/init.d/uhttpd restart
```

Después, recarga LuCI con `Ctrl+Shift+R` para forzar la recarga del CSS y el JS.

## Directivas de diseño gráfico (SaaS Dark)

- Fondo azul muy oscuro (`#060d1a`, `#0d1627`).
- Cards con glassmorphism sutil, borde tenue y `border-radius` ≥ 12 px.
- Gradientes de acento púrpura→azul (`#7c3aed` → `#2563eb`) en CTA y elementos de foco.
- Tipografías display: `Sora`, `DM Sans`, `Outfit`, `Plus Jakarta Sans`.
- Jerarquía visual con sidebar fija, header superior y grid de KPIs responsive.
- Hover/transiciones suaves (`transition: … 0.15s ease`) y microanimaciones de entrada.
- Se evita Bootstrap como base, neumorphism agresivo y grises planos sin matiz.
- Sin `backdrop-filter: blur()` (causaba difuminado global en LuCI).

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

## Arquitectura del menú (cliente)

LuCI construye el menú dinámicamente en JavaScript, no en el servidor. El flujo es:

1. `footer.htm` ejecuta `L.require('menu-saas-dark')`.
2. `menu-saas-dark.js` carga `require(['ui'])`, pide el árbol con `ui.menu.load()`.
3. Renderiza:
   - `renderModeMenu(tree)` → selector superior en `#modemenu`.
   - `renderMainMenu(child, name)` → listado vertical expandible en `#topmenu`.
   - `renderSubMenu(tree, url)` → pestañas en `#tabmenu`.

Si el árbol no llega (error de red o permisos), el usuario sigue viendo el shell del theme sin bloqueos.

## Modal y overlays

- `.modal` se estiliza como **card centrada** (`width: 90%; margin: 5em auto; max-width: 600px;`), **no** como overlay a pantalla completa.
- `#modal_overlay` es el backdrop real: `position: fixed`, oculto por defecto con `opacity: 0; visibility: hidden; pointer-events: none;`.
- Solo cuando LuCI añade `body.modal-overlay-active` se vuelve visible e interactivo.

Este patrón replica el del theme `luci-theme-bootstrap` y evita que el DOM del overlay bloquee los clics cuando está inactivo.
