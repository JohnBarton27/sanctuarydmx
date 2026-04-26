import argparse
import asyncio
from enum import Enum

import evdev
from evdev import ecodes
import websocket

QLC_WS = "ws://localhost:9999/qlcplusWS"

DEVICE_NAME_SUBSTRING = "Composite Device Keyboard"  # partial match, case-insensitive

DIMMER_WIDGET_ID = 13   # VirtualConsole "Both" dimmer slider (controls both fixtures)
BRIGHTNESS_STEP = 13   # ~5% of 255


class QlcFunctions(Enum):
    BLACKOUT = 4
    RED = 0
    GREEN = 1
    BLUE = 2
    LIGHT_BLUE = 3
    WHITE = 10
    PINK = 11
    AMBER = 12
    WARM_WHITE = 13
    TEAL = 14
    PURPLE = 15


# Map evdev key code → QLC+ function
# Use KEY_* constants from evdev.ecodes, e.g. ecodes.KEY_1, ecodes.KEY_F1
BUTTON_MAP = {
    ecodes.KEY_A: QlcFunctions.BLACKOUT,
    ecodes.KEY_B: QlcFunctions.WHITE,
    ecodes.KEY_C: QlcFunctions.PINK,
    ecodes.KEY_D: QlcFunctions.RED,
    ecodes.KEY_E: QlcFunctions.AMBER,
    ecodes.KEY_F: QlcFunctions.WARM_WHITE,
    ecodes.KEY_G: QlcFunctions.GREEN,
    ecodes.KEY_H: QlcFunctions.TEAL,
    ecodes.KEY_I: QlcFunctions.LIGHT_BLUE,
    ecodes.KEY_J: QlcFunctions.BLUE,
    ecodes.KEY_K: QlcFunctions.PURPLE,
    ecodes.KEY_L: "FX1",
    ecodes.KEY_1: "BRIGHT-",
    ecodes.KEY_2: "BRIGHT_PUSH",
    ecodes.KEY_3: "BRIGHT+",
    ecodes.KEY_4: "BOTTOM_KNOB_LEFT",
    ecodes.KEY_5: "BOTTOM_KNOB_PUSH",
    ecodes.KEY_6: "BOTTOM_KNOB_RIGHT"
}


current_function = None
brightness = 255


def fire_qlc_function(qlc_function):
    global current_function, brightness
    print(f"Firing {qlc_function}")

    if isinstance(qlc_function, QlcFunctions):
        ws = websocket.create_connection(QLC_WS)
        if current_function is not None and current_function != qlc_function:
            ws.send(f"QLC+API|setFunctionStatus|{current_function.value}|0")
        ws.send(f"QLC+API|setFunctionStatus|{qlc_function.value}|255")
        ws.close()
        current_function = qlc_function
    elif qlc_function in ("BRIGHT+", "BRIGHT-"):
        delta = BRIGHTNESS_STEP if qlc_function == "BRIGHT+" else -BRIGHTNESS_STEP
        brightness = max(0, min(255, brightness + delta))
        print(f"\tBrightness: {round(brightness / 255 * 100)}%")
        ws = websocket.create_connection(QLC_WS)
        ws.send(f"{DIMMER_WIDGET_ID}|{brightness}")
        ws.close()
    else:
        print("\tUnable to actually fire - this is not defined as a QlcFunction (yet!)")


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
                try:
                    if code in BUTTON_MAP:
                        fire_qlc_function(BUTTON_MAP[code])
                    else:
                        print(f"Unmapped key: {key_event.keycode} (code {code})")
                except Exception as e:
                    print(f"Error handling key {key_event.keycode}: {e}")


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

    ws = websocket.create_connection(QLC_WS)
    ws.send(f"{DIMMER_WIDGET_ID}|{brightness}")
    ws.close()

    asyncio.run(read_events(device))


if __name__ == "__main__":
    main()
