# AUTOMAIL (Requires Python 3.10+)

This is a solo project developed by @just-javing-pedro and published on GitHub. [See the project](https://github.com/just-javing-pedro/automail-app)

Follow me on [Tiktok](https://www.tiktok.com/@ppryan_mano?_r=1&_t=ZS-96zwOfjlFly)!

## HOW TO INSTALL

###  PYTHON DEPENDENCIES (All Systems)

```bash
pip install mailersend
```

### DEPENDENCIES - WINDOWS 10 / WINDOWS 11

#### PACMAN -S (Requires MSYS2 MinGW64 terminal)

```bash
pacman -S mingw-w64-x86_64-gtk3 mingw-w64-x86_64-python-gobject
```

### DEPENDENCIES - MACOS

#### BREW INSTALL

```bash
brew install gtk+3 glade pygobject3
```

### DEPENDENCIES - LINUX (UBUNTU / DEBIAN / MINT)

#### SUDO APT INSTALL

```bash
sudo apt update
sudo apt install python3-gi gir1.2-gtk-3.0 glade
```

### DEPENDENCIES - LINUX (FEDORA)

#### SUDO DNF INSTALL

```bash
sudo dnf install python3-gobject gtk3 glade
```

### DEPENDENCIES - LINUX (ARCH / MANJARO)

#### SUDO PACMAN -S

```bash
sudo pacman -S python-gobject gtk3 glade
```

## HOW TO RUN

```bash
python app.py
```