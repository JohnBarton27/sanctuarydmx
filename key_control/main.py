import argparse
import asyncio
from enum import Enum

import evdev
from evdev import ecodes
import websocket

QLC_WS = "ws://localhost:9999/qlcplusWS"

DEVICE_NAME_SUBSTRING = "macro"  # partial match, case-insensitive — adjust to your keypad's name


class QlcFunctions(Enum):
    BLACKOUT = 4
    RED = 0
    GREEN = 1
    BLUE = 2
    LIGHT_BLUE = 3


# Map evdev key code → QLC+ function
# Use KEY_* constants from evdev.ecodes, e.g. ecodes.KEY_1, ecodes.KEY_F1
BUTTON_MAP = {
    ecodes.KEY_1: QlcFunctions.BLACKOUT,
}


def fire_qlc_function(qlc_function):
    print(f"Firing {qlc_function}")
    ws = websocket.create_connection(QLC_WS)
    ws.send(f"QLC+API|setFunctionStatus|{qlc_function.value}|255")
    ws.close()


def list_devices():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    if not devices:
        print("No input devices found.")
        return
    print(f"{'Path':<25} {'Name':<40} {'Phys'}")
    print("-" * 80)
    for d in devices:
        print(f"{d.path:<25} {d.name:<40} {d.phys}")


def find_device(name_substring):
    for path in evdev.list_devices():
        d = evdev.InputDevice(path)
        if name_substring.lower() in d.name.lower():
            return d
    return None


async def read_events(device):
    print(f"Listening on: {device.path} ({device.name})")
    print("Press Ctrl+C to stop.")
    async for event in device.async_read_loop():
        if event.type == ecodes.EV_KEY:
            key_event = evdev.categorize(event)
            if key_event.keystate == evdev.KeyEvent.key_down:
                code = key_event.scancode
                if code in BUTTON_MAP:
                    fire_qlc_function(BUTTON_MAP[code])
                else:
                    print(f"Unmapped key: {key_event.keycode} (code {code})")


def main():
    parser = argparse.ArgumentParser(description="Macro keypad → QLC+ DMX controller")
    parser.add_argument("--list-devices", action="store_true", help="List all input devices and exit")
    parser.add_argument("--device", help="Device path (e.g. /dev/input/event5); auto-detected if omitted")
    args = parser.parse_args()

    if args.list_devices:
        list_devices()
        return

    if args.device:
        device = evdev.InputDevice(args.device)
    else:
        device = find_device(DEVICE_NAME_SUBSTRING)
        if device is None:
            print(f"No device found matching '{DEVICE_NAME_SUBSTRING}'. Run with --list-devices to see options.")
            return

    asyncio.run(read_events(device))


if __name__ == "__main__":
    main()
