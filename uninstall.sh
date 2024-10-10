#!/bin/bash


INSTALL_DIR="/opt/GG-Asus-Fan-Control"
SERVICE_FILE="gg-asus-fan-control.service"  
SYMLINK="/usr/local/bin/GG-Fan"


sudo systemctl stop "$SERVICE_FILE"
sudo systemctl disable "$SERVICE_FILE"


sudo rm /etc/systemd/system/"$SERVICE_FILE"
sudo systemctl daemon-reload


sudo rm -f "$SYMLINK"


sudo rm -rf "$INSTALL_DIR"

echo "Deinstallation abgeschlossen. GG Asus Fan Control wurde entfernt."
