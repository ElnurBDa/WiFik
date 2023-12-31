# WiFik: WiFi Security Testing Tool
## What is WiFik?
WiFik is an automated tool designed to test WiFi security conveniently by integrating with aircrack-ng. It simplifies the process of assessing the security of wireless networks, making it accessible for security professionals and enthusiasts alike.

## Features
Easy-to-use interface for selecting network interfaces and targets.
Automated detection and handling of WiFi devices.
Integration with popular wireless security tool aircrack-ng.
Detailed capture and analysis of WiFi Access Points and associated devices.

## Dependencies
Ensure these are installed before running WiFik:
```bash
sudo apt install xterm
sudo apt install aircrack-ng
```

## Installation and Setup
Clone the WiFik repository from GitHub.
Navigate into the WiFik directory.
Install the required dependencies as listed above.

## Usage
To start WiFik, run the following command:

```bash
sudo python WiFik.py
```

### Steps:
- Start WiFi Cracking: Initiates the process to select WiFi interface, scan for targets, and commence cracking.
- Choose Steps Again: Allows users to navigate back and choose specific steps in the WiFi cracking process.
- Exit: Terminates the application.

## Note
After using WiFik, it's recommended to restart your network adapters or PC to ensure all changes are reset, and devices return to their original state.

## Contributing
Contributions to WiFik are welcome! Whether it's feature enhancements, bug fixes, or documentation, feel free to fork the repository, make your changes, and submit a pull request.

## Disclaimer
WiFik is intended for educational and ethical testing purposes only. Users are responsible for adhering to all applicable laws and regulations regarding network access and testing. The developers assume no liability for misuse of the tool.