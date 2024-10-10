#!/bin/python3
import sys
import subprocess
import time
import os
import glob

# Metadata
version = "3.0.1"
author = "Gerald Hasani"
name = "GG-Asus-Fan-Control"
email = "contact@gerald-hasani.com"
github = "https://github.com/Gerald-Ha"
config_file = os.path.expanduser("~/.gg-asus-fan-control.conf")  

def get_hwmon_path():
    """Finds the correct hwmon path for asus-nb-wmi dynamically."""
    base_path = "/sys/devices/platform/asus-nb-wmi/hwmon/"
    hwmon_paths = glob.glob(base_path + "hwmon*")
    if hwmon_paths:
        return hwmon_paths[0]  
    else:
        print("Error: hwmon path not found.")
        sys.exit(1)

def get_k10temp_temperature():
    try:
        debug = subprocess.getoutput("sensors | grep 'Tctl'")
        temp_value = float(debug.split(":")[1].strip().split('\xb0')[0])
        return temp_value
    except Exception as debug:
        return None

def set_fan_speed(percentage, hwmon_path):
    pwm_value = 0 if percentage == 100 else 2
    command = f'echo {pwm_value} | sudo tee {hwmon_path}/pwm2_enable'
    os.system(command)

def set_fan_mode(mode, hwmon_path):
    if mode == "auto":
        command = f'echo 2 | sudo tee {hwmon_path}/pwm2_enable'
    elif mode == "full":
        command = f'echo 0 | sudo tee {hwmon_path}/pwm2_enable'
    os.system(command)

def save_choice(choice):
    with open(config_file, "w") as file:
        file.write(choice)

def load_choice():
    if os.path.exists(config_file):
        with open(config_file, "r") as file:
            return file.read().strip()
    return None

def monitor_temperature(interval=3):
    hwmon_path = get_hwmon_path()  
    while True:
        current_temp = get_k10temp_temperature()
        if current_temp is not None:
            if current_temp >= 82:
                set_fan_mode("full", hwmon_path)
            elif current_temp >= 65:
                set_fan_speed(60, hwmon_path)
            else:
                set_fan_mode("auto", hwmon_path)
        time.sleep(interval)

def start_service_mode():
    choice = load_choice()
    hwmon_path = get_hwmon_path()  
    if choice == "gg-modus":
        print("Starting GG-Modus based on previous selection.")
        monitor_temperature(interval=4)
    elif choice == "system":
        print("Starting System Modus based on previous selection.")
        set_fan_mode("auto", hwmon_path)

def main():
    ascii_art = r"""
  ____  ____       _____           
 / ___|/ ___|     |  ___|_ _ _ __  
| |  _| |  _ _____| |_ / _` | '_ \ 
| |_| | |_| |_____|  _| (_| | | | |
 \____|\____|     |_|  \__,_|_| |_|

    """
    print(ascii_art)
    print()
    
    
    if "--service" in sys.argv:
        start_service_mode()
        sys.exit(0)

    print("Please choose an option:")
    print()
    print("1. System Modus")
    print("2. GG-Modus")
    print()
    choice = input("Enter the number of your choice: ")
    hwmon_path = get_hwmon_path()  
    if choice == "1":
        set_fan_mode("auto", hwmon_path)
        save_choice("system")
        print("Fan control set to system control mode. Fan will operate automatically.")
    elif choice == "2":
        save_choice("gg-modus")
        print("GG-Modus Activated")
       
        pid = os.fork()
        if pid == 0:
           
            monitor_temperature(interval=4)
        else:
            
            sys.exit(0)
    else:
        print("Invalid choice. Please run the script again and choose a valid option.")

if __name__ == "__main__":
    main()
