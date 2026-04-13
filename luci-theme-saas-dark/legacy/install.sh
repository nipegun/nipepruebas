#!/usr/bin/env sh

set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
DEST_ROOT="${1:-/}"

copy_file() {
    src="$1"
    dst="$2"
    mode="$3"

    src_path="$SCRIPT_DIR/$src"
    dst_path="$DEST_ROOT/$dst"

    if [ ! -f "$src_path" ]; then
        echo "[ERROR] No se encontró: $src_path" >&2
        exit 1
    fi

    install -D -m "$mode" "$src_path" "$dst_path"
    echo "[OK] $src -> /$dst"
}

echo "Instalando luci-theme-saas-dark (legacy) en: $DEST_ROOT"

# Templates LuCI
copy_file "luasrc/view/themes/saas-dark/header.htm"  "usr/lib/lua/luci/view/themes/saas-dark/header.htm"  "0644"
copy_file "luasrc/view/themes/saas-dark/footer.htm"  "usr/lib/lua/luci/view/themes/saas-dark/footer.htm"  "0644"
copy_file "luasrc/view/themes/saas-dark/sysauth.htm" "usr/lib/lua/luci/view/themes/saas-dark/sysauth.htm" "0644"

# Assets estáticos del tema
copy_file "htdocs/luci-static/saas-dark/css/style.css" "www/luci-static/saas-dark/css/style.css" "0644"
copy_file "htdocs/luci-static/saas-dark/js/theme.js"   "www/luci-static/saas-dark/js/theme.js"   "0644"

# Módulo JS del menú
copy_file "htdocs/luci-static/resources/menu-saas-dark.js" "www/luci-static/resources/menu-saas-dark.js" "0644"

# UCI defaults
copy_file "root/etc/uci-defaults/99-theme-saas-dark" "etc/uci-defaults/99-theme-saas-dark" "0755"

echo ""
echo "Instalación completada."
echo "Si estás instalando directo en el router, aplica el theme con:"
echo "  uci set luci.main.mediaurlbase='/luci-static/saas-dark'"
echo "  uci commit luci"
echo "  /etc/init.d/uhttpd restart"
