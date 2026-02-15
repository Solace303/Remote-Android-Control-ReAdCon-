import subprocess
import time
import threading
import re
import os
from pynput import mouse, keyboard

# ---------------- CONFIG ----------------
DEVICE_WIDTH = 1080
DEVICE_HEIGHT = 1920
WINDOW_WIDTH = 540
WINDOW_HEIGHT = 960
DEVICE_FILE = "/home/solace/Bot/Remote_Android_Control/devices.txt"
ADB_PORT = 5555
# ---------------------------------------


# ---------- DEVICE HELPERS ----------
def run(cmd):
    return subprocess.check_output(cmd, shell=True).decode(errors="ignore")


def get_usb_device():
    out = run("adb devices")
    for line in out.splitlines():
        if "\tdevice" in line:
            return line.split()[0]
    return None


def get_device_ip(device):
    out = run(f"adb -s {device} shell ip addr show wlan0")
    match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)', out)
    return match.group(1) if match else None


def get_imei(device):
    try:
        cmd = (
            f'adb -s {device} shell '
            'service call iphonesubinfo 1 | '
            'grep -oE "[0-9]+" | tr -d "\\n"'
        )
        return run(cmd).strip()
    except:
        return "UNKNOWN"


def save_device(name, ip, imei):
    entry = f"{name}|{ip}|{imei}"

    if not os.path.exists(DEVICE_FILE):
        open(DEVICE_FILE, "w").close()

    with open(DEVICE_FILE, "r") as f:
        if entry in f.read():
            print("⚠️  already saved device")
            return False

    with open(DEVICE_FILE, "a") as f:
        f.write(entry + "\n")

    print("✅ Device saved")
    return True


def load_devices():
    if not os.path.exists(DEVICE_FILE):
        return []

    with open(DEVICE_FILE, "r") as f:
        return [line.strip().split("|") for line in f if line.strip()]


# ---------- SCRCPY ----------
def start_scrcpy(device):
    subprocess.Popen([
        "scrcpy",
        "-s", device,
        "--window-title", "Readcon",
        "--window-width", str(WINDOW_WIDTH),
        "--window-height", str(WINDOW_HEIGHT),
        "--always-on-top"
    ])


# ---------- INPUT CONTROL ----------
def on_click(x, y, button, pressed):
    if pressed:
        dx = int(x * (DEVICE_WIDTH / WINDOW_WIDTH))
        dy = int(y * (DEVICE_HEIGHT / WINDOW_HEIGHT))
        subprocess.run(f"adb shell input tap {dx} {dy}", shell=True)


def on_press(key, device):
    try:
        if key == keyboard.KeyCode.from_char('='):
            subprocess.run(f"adb -s {device} shell input keyevent 24", shell=True)
        elif key == keyboard.KeyCode.from_char('-'):
            subprocess.run(f"adb -s {device} shell input keyevent 25", shell=True)
        elif key == keyboard.Key.f6:
            subprocess.run(f"adb -s {device} shell input keyevent 26", shell=True)
    except:
        pass


# ---------- MODES ----------
def connect_new_device():
    device = get_usb_device()
    if not device:
        print("❌ No USB device detected")
        return

    print(f"📱 USB device: {device}")

    run(f"adb -s {device} tcpip {ADB_PORT}")
    time.sleep(1)

    ip = get_device_ip(device)
    if not ip:
        print("❌ Failed to get device IP")
        return

    run(f"adb connect {ip}:{ADB_PORT}")

    imei = get_imei(device)
    save_device(device, ip, imei)

    launch(device=f"{ip}:{ADB_PORT}")


def connect_old_device():
    devices = load_devices()
    if not devices:
        print("❌ No saved devices")
        return

    print("\nSaved devices:")
    for i, d in enumerate(devices):
        print(f"{i+1}. {d[0]} @ {d[1]}")

    choice = int(input("Select device: ")) - 1
    name, ip, imei = devices[choice]

    run(f"adb connect {ip}:{ADB_PORT}")
    launch(device=f"{ip}:{ADB_PORT}")


def launch(device):
    scrcpy_thread = threading.Thread(target=start_scrcpy, args=(device,))
    scrcpy_thread.start()

    mouse_listener = mouse.Listener(on_click=on_click)
    keyboard_listener = keyboard.Listener(
        on_press=lambda key: on_press(key, device)
    )

    mouse_listener.start()
    keyboard_listener.start()

    mouse_listener.join()
    keyboard_listener.join()
    
def exit_program():
    print("Exiting...")
    os._exit(0)


# ---------- MAIN ----------
if __name__ == "__main__":
    while True:
        print("""
    1. Connect new device
    2. Connect old device
    3. Exit Program
    """)

        option = input("Select option: ").strip()

        try:
            if option == "1":
                connect_new_device()
            elif option == "2":
                connect_old_device()
            elif option == "3":
                exit_program()
            else:
                print("Invalid option")
                continue
        except Exception as e:
            print(f"Error: {e}")
            continue