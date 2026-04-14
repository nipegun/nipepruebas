#!/bin/bash

set -euo pipefail

cBaseURL="https://raw.githubusercontent.com/nipegun/nipepruebas/main/luci-theme-saas-dark/modern"
cTempDir=""

fCleanup() {
  if [ -n "$cTempDir" ] && [ -d "$cTempDir" ]; then
    rm -rf "$cTempDir"
  fi
}

trap fCleanup EXIT

fDescargar() {
  local pOrigen="$1"
  local pDestino="$2"
  local pPermisos="$3"
  local vURL="${cBaseURL}/${pOrigen}"
  local vTmp="${cTempDir}/descarga.tmp"

  echo "  Descargando: ${pOrigen}"
  if ! curl -fsSL -o "$vTmp" "$vURL"; then
    echo "[ERROR] No se pudo descargar: ${vURL}" >&2
    return 1
  fi

  local vDirDestino
  vDirDestino="$(dirname "$pDestino")"
  mkdir -p "$vDirDestino"
  mv "$vTmp" "$pDestino"
  chmod "$pPermisos" "$pDestino"
  echo "  [OK] -> ${pDestino}"
}

fMain() {

  echo ""
  echo "============================================="
  echo "  luci-theme-saas-dark v2.0.0 (modern)"
  echo "  Compatible con OpenWrt 25.12.x y superior"
  echo "============================================="
  echo ""

  # Comprobar que curl está disponible
  if ! command -v curl > /dev/null 2>&1; then
    echo "[ERROR] curl no está instalado. Ejecuta: apk add curl" >&2
    return 1
  fi

  # Comprobar que estamos en un sistema OpenWrt
  if [ ! -f /etc/openwrt_release ]; then
    echo "[ERROR] Este script debe ejecutarse en un router OpenWrt." >&2
    return 1
  fi

  cTempDir="$(mktemp -d)"

  echo "Descargando archivos del tema..."
  echo ""

  # Templates LuCI
  fDescargar "luasrc/view/themes/saas-dark/header.htm"  "/usr/lib/lua/luci/view/themes/saas-dark/header.htm"  "0644"
  fDescargar "luasrc/view/themes/saas-dark/footer.htm"  "/usr/lib/lua/luci/view/themes/saas-dark/footer.htm"  "0644"
  fDescargar "luasrc/view/themes/saas-dark/sysauth.htm" "/usr/lib/lua/luci/view/themes/saas-dark/sysauth.htm" "0644"

  # Assets estáticos del tema
  fDescargar "htdocs/luci-static/saas-dark/css/style.css" "/www/luci-static/saas-dark/css/style.css" "0644"
  fDescargar "htdocs/luci-static/saas-dark/js/theme.js"   "/www/luci-static/saas-dark/js/theme.js"   "0644"

  # Módulo JS del menú (se instala en resources, junto a menu-bootstrap.js)
  fDescargar "htdocs/luci-static/resources/menu-saas-dark.js" "/www/luci-static/resources/menu-saas-dark.js" "0644"

  # UCI defaults
  fDescargar "root/etc/uci-defaults/99-theme-saas-dark" "/etc/uci-defaults/99-theme-saas-dark" "0755"

  echo ""
  echo "Aplicando configuración UCI..."

  # Registrar el theme en luci.themes.* para que aparezca en el dropdown "Diseño"
  uci -q delete luci.themes.SaaSDark
  uci -q set luci.themes.SaaSDark='/luci-static/saas-dark'

  # Activar el theme como actual
  uci -q set luci.main.mediaurlbase='/luci-static/saas-dark'
  uci -q commit luci

  echo ""
  echo "Reiniciando uhttpd..."

  /etc/init.d/uhttpd restart

  echo ""
  echo "============================================="
  echo "  Instalación completada."
  echo "  El tema SaaS Dark ya está activo en LuCI."
  echo "============================================="
  echo ""
}

if ! fMain; then
  echo ""
  echo "[ERROR] La instalación falló." >&2
fi
