# Remote Android Control - ReAdCon

A Linux-based tool for controlling Android devices remotely using ADB and scrcpy.

## Requirements
- Linux operating system
- ADB (Android Debug Bridge)
- scrcpy (screen mirroring tool)
- Python 3.x
- pynput library (`pip install pynput`)

## Installation
1. Install ADB and scrcpy:
sudo apt update
sudo apt install adb scrcpy

2. Install required Python package:
pip install -r requirements.txt

## Usage
1. Run the script:
python remote_control.py

2. Select an option:
    - 1: Connect new device
    - 2: Connect old device
    - 3: Exit Program

## Features
- Connect to Android devices via USB or Wi-Fi
- Mirror device screen using scrcpy
- Control device using mouse and keyboard
- Save device connections for future use

## Controls
- `=` : Volume up
- `-` : Volume down
- `F6` : Power button

## Notes
- Make sure USB debugging is enabled on your Android device
- Ensure scrcpy is installed and configured properly
