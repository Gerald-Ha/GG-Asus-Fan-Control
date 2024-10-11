#!/usr/bin/env python3
import sys
import subprocess
import time
import os

# Metadata
version = "3.0.4"
author = "Gerald Hasani"
name = "GG-Asus-Fan-Control"
email = "contact@gerald-hasani.com"
github = "https://github.com/Gerald-Ha"
config_file = os.path.expanduser("~/.gg-asus-fan-control.conf")

# Temperatur-Schwellenwerte für die verschiedenen Modi
GG_MODE_THRESHOLD = 84  # Temperatur in Grad Celsius für GG-Mode
GAMING_MODE_THRESHOLD = 70  # Temperatur in Grad Celsius für Gaming Mode

def print_ascii_art():
    CYAN = "\033[36m"
    RESET = "\033[0m"

    ascii_art = r"""
  ____  ____       _____           
 / ___|/ ___|     |  ___|_ _ _ __  
| |  _| |  _ _____| |_ / _  | '_ \ 
| |_| | |_| |_____|  _| (_| | | | |
 \____|\____|     |_|  \__,_|_| |_|

    """
    print(f"{CYAN}{ascii_art}{RESET}")
    print()

def get_k10temp_temperature():
    try:
        output = subprocess.getoutput("sensors | grep 'Tctl'")
        temp_value = float(output.split(":")[1].strip().split('°')[0])
        return temp_value
    except Exception:
        return None

def set_fan_speed_manual(mode):
    hwmon_dirs = [d for d in os.listdir("/sys/devices/platform/asus-nb-wmi/hwmon/") if d.startswith("hwmon")]
    if not hwmon_dirs:
        print("Kein gültiges hwmon-Verzeichnis gefunden.")
        return

    hwmon_dir = hwmon_dirs[0]
    pwm1_enable_path = f'/sys/devices/platform/asus-nb-wmi/hwmon/{hwmon_dir}/pwm1_enable'

    if mode == "full":
        value = '0'
    elif mode == "auto":
        value = '2'
    else:
        print("Unbekannter Modus")
        return

    try:
        with open(pwm1_enable_path, 'w') as f:
            f.write(value)
    except Exception as e:
        print(f"Fehler beim Setzen der Lüftergeschwindigkeit: {e}")

def save_choice(choice):
    with open(config_file, "w") as file:
        file.write(choice)

def load_choice():
    try:
        with open(config_file, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return "system"

def monitor_temperature(mode, interval=3):
    while True:
        current_temp = get_k10temp_temperature()
        if current_temp is not None:
            if mode == "gaming" and current_temp >= GAMING_MODE_THRESHOLD:
                set_fan_speed_manual("full")
            elif mode == "gg" and current_temp >= GG_MODE_THRESHOLD:
                set_fan_speed_manual("full")
            else:
                set_fan_speed_manual("auto")
        time.sleep(interval)

def main():
    print_ascii_art()

    current_mode = load_choice()
    mode_display = {
        "system": "System Mode",
        "gg-mode": "GG-Mode",
        "gaming-mode": "Gaming Mode"
    }
    current_mode_display = mode_display.get(current_mode, "Unknown Mode")
    print(f"Aktueller Modus: {current_mode_display}")
    print()

    if "--service" in sys.argv:
        choice = load_choice()
        if choice == "gg-mode":
            print("GG-Mode wird als Service aktiviert.")
            monitor_temperature("gg", interval=4)
        elif choice == "gaming-mode":
            print("Gaming Mode wird als Service aktiviert.")
            monitor_temperature("gaming", interval=4)
        else:
            set_fan_speed_manual("auto")
        return

    print("Bitte wählen Sie eine Option:")
    print()
    print("1. System Mode")
    print("2. GG-Mode")
    print("3. Gaming Mode")
    print()
    choice = input("Geben Sie die Nummer Ihrer Wahl ein: ")
    print()
    if choice == "1":
        save_choice("system")
        set_fan_speed_manual("auto")
        print("Lüftersteuerung auf Systemmodus gesetzt. Der Lüfter arbeitet automatisch.")
        
        os.system("sudo systemctl stop gg-asus-fan-control.service")
    elif choice == "2":
        save_choice("gg-mode")
        print("GG-Mode aktiviert")
        
        os.system("sudo systemctl restart gg-asus-fan-control.service")
    elif choice == "3":
        save_choice("gaming-mode")
        print("Gaming Mode aktiviert")
        
        os.system("sudo systemctl restart gg-asus-fan-control.service")
    else:
        print("Ungültige Auswahl. Bitte führen Sie das Skript erneut aus und wählen Sie eine gültige Option.")

if __name__ == "__main__":
    main()
