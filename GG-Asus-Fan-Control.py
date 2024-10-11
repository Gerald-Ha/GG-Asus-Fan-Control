#!/bin/python3
import sys
import subprocess
import time
import os
import signal

# Metadata
version = "3.0.3"
author = "Gerald Hasani"
name = "GG-Asus-Fan-Control"
email = "contact@gerald-hasani.com"
github = "https://github.com/Gerald-Ha"
config_file = os.path.expanduser("~/.gg-asus-fan-control.conf")  
pid_file = os.path.expanduser("~/.gg-asus-fan-control.pid")  

# Temperatur-Schwellenwerte für die verschiedenen Modi
GG_MODE_THRESHOLD = 84  # Temperatur in Grad Celsius für GG-Mode
GAMING_MODE_THRESHOLD = 70  # Temperatur in Grad Celsius für Gaming Mode

def print_ascii_art():
    
    CYAN = "\033[36m"
    RESET = "\033[0m"  

    ascii_art = r"""
  ____  ____       _____           
 / ___|/ ___|     |  ___|_ _ _ __  
| |  _| |  _ _____| |_ / _` | '_ \ 
| |_| | |_| |_____|  _| (_| | | | |
 \____|\____|     |_|  \__,_|_| |_|

    """
    print(f"{CYAN}{ascii_art}{RESET}")
    print()

def get_k10temp_temperature():
    try:
        debug = subprocess.getoutput("sensors | grep 'Tctl'")
        temp_value = float(debug.split(":")[1].strip().split('\xb0')[0])
        return temp_value
    except Exception as debug:
        return None

def set_fan_speed_manual(mode):
    
    hwmon_dirs = [d for d in os.listdir("/sys/devices/platform/asus-nb-wmi/hwmon/") if d.startswith("hwmon")]
    if not hwmon_dirs:
        print("Kein gültiges hwmon-Verzeichnis gefunden.")
        return
    
    hwmon_dir = hwmon_dirs[0]
    
    if mode == "full":
        command = f'echo 0 | sudo tee /sys/devices/platform/asus-nb-wmi/hwmon/{hwmon_dir}/pwm1_enable'
    elif mode == "auto":
        command = f'echo 2 | sudo tee /sys/devices/platform/asus-nb-wmi/hwmon/{hwmon_dir}/pwm1_enable'
    os.system(command)

def save_choice(choice):
    with open(config_file, "w") as file:
        file.write(choice)

def load_choice():
    try:
        with open(config_file, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return "system"  

def save_pid(pid):
    with open(pid_file, "w") as file:
        file.write(str(pid))

def load_pid():
    try:
        with open(pid_file, "r") as file:
            return int(file.read().strip())
    except FileNotFoundError:
        return None

def stop_monitoring():
    pid = load_pid()
    if pid:
        try:
            os.kill(pid, signal.SIGTERM)
            os.remove(pid_file)
            print("Monitoring process stopped.")
        except ProcessLookupError:
            print("No running monitoring process found.")
        except Exception as e:
            print(f"Error stopping the process: {e}")
    else:
        print("No monitoring process recorded.")

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
    print(f"Current Mode: {current_mode_display}")
    print()  

    if "--service" in sys.argv:
        choice = load_choice()
        if choice == "gg-mode":
            print("GG-Mode is being activated as a service.")
            pid = os.fork()
            if pid == 0:
                monitor_temperature("gg", interval=4)
            else:
                save_pid(pid)
                sys.exit(0)
        elif choice == "gaming-mode":
            print("Gaming Mode is being activated as a service.")
            pid = os.fork()
            if pid == 0:
                monitor_temperature("gaming", interval=4)
            else:
                save_pid(pid)
                sys.exit(0)
        else:
            set_fan_speed_manual("auto")
        return

    print("Please choose an option:")
    print()  
    print("1. System Mode")
    print("2. GG-Mode")
    print("3. Gaming Mode")
    print()  
    choice = input("Enter the number of your choice: ")
    print()  
    if choice == "1":
        stop_monitoring()
        set_fan_speed_manual("auto")
        save_choice("system")
        print("Fan control set to system control mode. Fan will operate automatically.")
    elif choice == "2":
        stop_monitoring()
        save_choice("gg-mode")
        print("GG-Mode Activated")
        pid = os.fork()
        if pid == 0:
            monitor_temperature("gg", interval=4)
        else:
            save_pid(pid)
            sys.exit(0)
    elif choice == "3":
        stop_monitoring()
        save_choice("gaming-mode")
        print("Gaming Mode Activated")
        pid = os.fork()
        if pid == 0:
            monitor_temperature("gaming", interval=4)
        else:
            save_pid(pid)
            sys.exit(0)
    else:
        print("Invalid choice. Please run the script again and choose a valid option.")

if __name__ == "__main__":
    main()
