
# GG Asus Fan Control

GG Asus Fan Control is a Python-based script specifically designed for Asus Vivobook notebooks, where regulated fan control is otherwise unavailable. The script provides two modes: **System Mode** and **GG Mode**, each designed to optimize cooling and performance based on the user’s choice.

![2024-10-10_17-16](https://github.com/user-attachments/assets/bc46e1ca-2626-47ad-a729-ebaa7908e2bb)



## Features

- **System Mode**: Relinquishes control to the system, letting it manage the fan speeds automatically.
- **GG Mode**: Monitors the system's temperature and dynamically adjusts fan speeds to maintain optimal performance.
- **Background Operation**: In GG Mode, the script runs as a background process, ensuring continuous monitoring without occupying the terminal.
- **User-Friendly Interface**: Simple command-line interface to choose between modes.

## Important Note

Due to hardware limitations, it is not possible to set the fan speed at specific percentages. Therefore, when the temperature reaches 82°C, the script activates the full fan mode to prevent overheating and extend the lifespan of the notebook.

## Installation

### Prerequisites

- Python 3
- `sensors` utility (part of the `lm-sensors` package)
- Root privileges (to control fan speeds)

### Install the Script

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/your-username/GG-Asus-Fan-Control.git
cd GG-Asus-Fan-Control
```

Run the installation script:

```bash
chmod +x install.sh
sudo ./install.sh
```

The installation script will:
- Copy the Python script to `/opt/GG-Asus-Fan-Control`.
- Create a symbolic link `/usr/local/bin/GG-Fan` for easy access.
- Set up a systemd service for background operation.
- The program starts automatically with the system and executes the last selected mode.

## Usage

To start GG Asus Fan Control, simply run:

```bash
sudo GG-Fan
```

You will be prompted to choose between the available modes:

1. **System Mode**: The system will manage the fan speeds automatically.
2. **GG Mode**: The script will actively monitor the temperature and adjust the fan speeds.

### Example

```
Please choose an option:
1. System Mode
2. GG Mode
Enter the number of your choice: 2
GG Mode Activated
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
GitHub: [https://github.com/Gerald-Ha](https://github.com/Gerald-Ha)
