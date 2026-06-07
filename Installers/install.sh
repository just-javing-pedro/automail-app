#!/bin/bash

AUTOMAIL_DIR="$(cd "$(dirname "$0")/../Automail" && pwd)"

echo "Identifying Package Manager..."

if command -v apt-get >/dev/null 2>&1; then
    PKG_MANAGER="apt"
elif command -v dnf >/dev/null 2>&1; then
    PKG_MANAGER="dnf"
elif command -v pacman >/dev/null 2>&1; then
    PKG_MANAGER="pacman"
else
    echo "Error: Package manager not supported."
    exit 1
fi

if [ "$PKG_MANAGER" = "apt" ]; then
    echo 'Enter your administrator password to allow the installation of the "python3-gi", "gir1.2-gtk-3.0", and "glade" packages:'
    sudo apt update
    sudo apt install -y python3-gi gir1.2-gtk-3.0 glade
elif [ "$PKG_MANAGER" = "dnf" ]; then
    echo 'Enter your administrator password to allow the installation of the "python3-gobject", "gtk3", and "glade" packages:'
    sudo dnf install -y python3-gobject gtk3 glade
elif [ "$PKG_MANAGER" = "pacman" ]; then
    echo 'Enter your administrator password to allow the installation of the "python3-gobject", "gtk3", and "glade" packages:'
    sudo pacman -S --needed --noconfirm python-gobject gtk3 glade
fi


echo "Creating .venv..."

python3 -m venv ${AUTOMAIL_DIR}/.venv

echo 'Installing dependencies via pip...'

"${AUTOMAIL_DIR}/.venv/bin/pip" install mailersend PyGObject

echo 'Creating "Automail.desktop"...'

cat > Automail.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Automail
Exec="${AUTOMAIL_DIR}/.venv/bin/python3" "${AUTOMAIL_DIR}/Automail_Program/app.py"
Icon=${AUTOMAIL_DIR}/Automail_UI/pics/Icon.svg
Terminal=false
Categories=Utility;
EOF

chmod +x Automail.desktop
mv Automail.desktop ~/.local/share/applications/

echo "Ready!"