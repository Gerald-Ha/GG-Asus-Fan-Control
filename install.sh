#!/bin/bash


INSTALL_DIR="/opt/GG-Asus-Fan-Control"
SERVICE_FILE="gg-asus-fan-control.service"
SYMLINK="/usr/local/bin/GG-Fan"


sudo mkdir -p "$INSTALL_DIR"


sudo cp GG-Asus-Fan-Control.py "$INSTALL_DIR/GG-Asus-Fan-Control.py"


sudo chmod +x "$INSTALL_DIR/GG-Asus-Fan-Control.py"


sudo cp "$SERVICE_FILE" /etc/systemd/system/


sudo systemctl daemon-reload
sudo systemctl enable "$SERVICE_FILE"
sudo systemctl start "$SERVICE_FILE"


sudo ln -sf "$INSTALL_DIR/GG-Asus-Fan-Control.py" "$SYMLINK"

echo "Installation abgeschlossen. Verwenden Sie 'GG-Fan' in der Konsole, um das Programm manuell zu starten."
