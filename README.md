# Remote Android Control - ReAdCon

A Linux-based tool for controlling Android devices remotely using ADB and scrcpy-server.

## Requirements
- Linux operating system
- ADB (Android Debug Bridge)
- scrcpy-server (screen mirroring tool)
- Python 3.x
- pynput library (`pip install pynput`)

## Installation
1. Install ADB:
```bash
sudo apt update
sudo apt install adb
```

2. Download and install scrcpy-server:
# Download scrcpy-server from official GitHub repository
wget https://github.com/Genymobile/scrcpy/releases/download/v1.24/scrcpy-server-v1.24

```bash
# Make the server executable
chmod +x scrcpy-server-v1.24

# Move the server to a directory in your PATH (e.g., /usr/local/bin/)
sudo mv scrcpy-server-v1.24 /usr/local/bin/scrcpy-server
```

3. Install required Python package:
 ```bash
pip install -r requirements.txt
```

## Usage
1. Run the script:
```bash
python ReAdCon.py
```

3. Select an option:
    - 1: Connect new device
    - 2: Connect old device
    - 3: Exit Program

## Features
- Connect to Android devices via USB or Wi-Fi
- Mirror device screen using scrcpy-server
- Control device using mouse and keyboard
- Save device connections for future use

## Controls
- `=` : Volume up
- `-` : Volume down
- `F6` : Power button

## Notes
- Make sure USB debugging is enabled on your Android device
- Ensure scrcpy-server is installed and configured properly
