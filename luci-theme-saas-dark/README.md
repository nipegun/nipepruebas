# luci-theme-saas-dark

`luci-theme-saas-dark` es un theme oscuro para LuCI orientado a OpenWrt `v25.12.2` y superiores.
Está diseñado para funcionar con el ecosistema actual de OpenWrt donde la instalación de paquetes en router se realiza con **apk** (no con opkg).

## Compatibilidad

- OpenWrt `v25.12.2+`.
- Buildroot oficial de OpenWrt para compilar el paquete LuCI.
- Instalación en router con `apk add` sobre paquetes `.apk`.

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

## Instalación directa en router (OpenWrt 25.12.x)

```sh
ssh root@192.168.1.1
cd /tmp
wget https://tu-servidor/paquetes/luci-theme-saas-dark_2.0.0_all.apk
apk add --allow-untrusted /tmp/luci-theme-saas-dark_2.0.0_all.apk
uci set luci.main.mediaurlbase='/luci-static/saas-dark'
uci commit luci
/etc/init.d/uhttpd restart
```

## Directivas de diseño gráfico (SaaS Dark)

- Fondo azul muy oscuro (`#050d1a`, `#080f1f`) o negro profundo.
- Cards con glassmorphism sutil, borde tenue y `border-radius` >= 16px.
- Gradientes de acento púrpura→azul (`#7c3aed` → `#2563eb`) en CTA y elementos de foco.
- Tipografías display: `Sora`, `DM Sans`, `Outfit`, `Plus Jakarta Sans`.
- Jerarquía visual con sidebar fija, header superior y grid de KPIs responsive.
- Hover/transiciones suaves (`transition: all 0.2s ease`) y microanimaciones de entrada.
- Evitar Bootstrap como base, neumorphism agresivo y grises planos sin matiz.

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
  --shadow-card:    0 8px 32px rgba(124, 58, 237, 0.10);
  --radius-card:    16px;
  --radius-btn:     10px;
}
```
