
# GG Asus Fan Control

GG Asus Fan Control is a Python-based script specifically designed for Asus Vivobook notebooks, where regulated fan control is otherwise unavailable. Many Asus Vivobooks have hardware limitations under Linux, preventing direct fan control through standard utilities. This script provides a solution by leveraging the `lm-sensors` package and root permissions to manage fan speeds effectively. The script provides three modes: **System Mode**, **GG Mode**, and **Gaming Mode**, each designed to optimize cooling and performance based on the user’s choice.

![2024-10-11_14-47](https://github.com/user-attachments/assets/61cc254f-a5a7-4c05-a470-4ed0263b01e0)

## Features

- **System Mode**: Relinquishes control to the system, letting it manage the fan speeds automatically.
- **GG Mode**: Monitors the system's temperature and dynamically adjusts fan speeds to maintain optimal performance. The default temperature threshold is 84°C.
- **Gaming Mode**: Sets the fan to 100% speed when the temperature reaches the configured threshold (default is 70°C), ensuring maximum cooling. When the temperature drops below this threshold, the system takes back control to adjust fan speed automatically.
- **Current Mode Display**: The current active mode is displayed when the script starts, providing users with information about the system's current status.
- **Customizable Temperature Thresholds**: The temperature thresholds for both GG Mode and Gaming Mode can be configured at the beginning of the script to fit user preferences.
- **Background Operation**: In GG and Gaming Modes, the script runs as a background process, ensuring continuous monitoring without occupying the terminal.
- **User-Friendly Interface**: Simple command-line interface to choose between modes.
- **Persistent Mode Configuration**: The script remembers the last selected mode and automatically applies it upon restart.

## How it Works

Due to the limitations of certain Asus Vivobook models under Linux, it is not possible to directly control the hardware for fan speed regulation. This script addresses that limitation by utilizing available sensor data and controlling the fan speed through system commands. By operating in the background, it ensures that the fan control remains active without manual intervention, providing a consistent cooling experience.

## Important Note

Due to hardware limitations, it is not possible to set the fan speed at specific percentages. Therefore, when the configured temperature threshold is reached, the script activates the full fan mode to prevent overheating and extend the lifespan of the notebook.

## Installation

### Prerequisites

- Python 3
- `sensors` utility (part of the `lm-sensors` package)
- Root privileges (to control fan speeds)

### Install the Script

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/Gerald-Ha/GG-Asus-Fan-Control.git
cd GG-Asus-Fan-Control
```

Run the installation script:

```bash
chmod +x install.sh
sudo ./install.sh
```

The installation script will:
- Copy the Python script to `/opt/GG-Asus-Fan-Control`.
- Create a symbolic link `/usr/local/bin/gg-fan` for easy access.
- Set up a systemd service for background operation.
- The program starts automatically with the system and executes the last selected mode.

## Usage

To start GG Asus Fan Control, simply run:

```bash
sudo gg-fan
```

You will be prompted to choose between the available modes:

1. **System Mode**: The system will manage the fan speeds automatically.
2. **GG Mode**: The script will actively monitor the temperature and adjust the fan speeds based on the configured threshold.
3. **Gaming Mode**: The script will set the fan to full speed when the temperature reaches the configured threshold (default 70°C) and will return control to the system when the temperature is below this threshold. This mode is designed for gaming sessions where the fan in GG Mode might frequently switch on and off.

### Example

```
Current Mode: System Mode

Please choose an option:
1. System Mode
2. GG Mode
3. Gaming Mode
Enter the number of your choice: 3
Gaming Mode Activated
```

## Uninstallation

To remove GG Asus Fan Control from your system, run:

```bash
chmod +x uninstall.sh
sudo ./uninstall.sh
```

The uninstallation script will:
- Stop and disable the systemd service.
- Remove the service file and symbolic link.
- Delete the installation directory.

## Configuration

The script saves the user’s mode selection in a configuration file located at `~/.gg-asus-fan-control.conf`. The configuration is automatically updated each time the script is run and a mode is selected.

### Changing Temperature Thresholds

The temperature thresholds for GG Mode and Gaming Mode can be adjusted at the top of the script by modifying the `GG_MODE_THRESHOLD` and `GAMING_MODE_THRESHOLD` variables. These values are persistent and will remain after a system restart.

## Troubleshooting

- **Permissions Issues**: Make sure you run the script with `sudo` as it requires root privileges to control fan speeds.
- **Fan Not Responding**: Ensure that the `lm-sensors` package is installed and configured correctly.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Gerald Hasani

Contact: [contact@gerald-hasani.com](mailto:contact@gerald-hasani.com)  
Gitea: [gitea.gerald-hasani.com/Gerald](https://gitea.gerald-hasani.com/Gerald)  
GitHub: [github.com/Gerald-Ha](https://github.com/Gerald-Ha)

