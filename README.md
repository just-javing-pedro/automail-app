# AUTOMAIL (Requires Python 3.10+)

This is a solo project developed by @just-javing-pedro and published on GitHub. [See the project](https://github.com/just-javing-pedro/automail-app/)

Follow me on [Tiktok](https://www.tiktok.com/@ppryan_mano?_r=1&_t=ZS-96zwOfjlFly)!

## HOW TO INSTALL
## HOW TO INSTALL - AUTOMATICALLY (Linux)

### Compatible with: Debian, Ubuntu, Mint, Fedora, Arch, Manjaro

Inside the folder where you installed the package:

```bash
cd automail-app
cd Installers
chmod +x install.sh
./install.sh
```

## HOW TO INSTALL - MANUALLY

###  PYTHON DEPENDENCIES (All Systems)

```bash
pip install mailersend
pip install PyGObject
```
Make sure you are in the correct directory and your environment is active.

### DEPENDENCIES - WINDOWS 10 / WINDOWS 11

@@ -55,6 +70,26 @@ sudo pacman -S python-gobject gtk3 glade

## HOW TO RUN

### If you used the **Automatic Installer**, you can simply open "Automail" from your Applications Menu.

### Else:

If you are in the **"Installers"** folder:

```bash
cd ../Automail
```

Next, run the command:

```bash
python app.py
```

Or, if you have a **.venv environment**:

```bash
./.venv/bin/python3 app.py
```

**(Or, depending on the case, "python3")**