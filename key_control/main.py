from enum import Enum
from gpiozero import Button
import time
import websocket

QLC_WS = "ws://localhost:9999/qlcplusWS"


class QlcFunctions(Enum):
    BLACKOUT = 4
    RED = 0
    GREEN = 1
    BLUE = 2
    LIGHT_BLUE = 3


# Map GPIO pin → QLC+ function ID
BUTTON_MAP = {
    4: QlcFunctions.BLACKOUT,   # GPIO4 → QLC function ID 1
}


def fire_qlc_function(qlc_function):
    print(f"Firing {qlc_function}")
    ws = websocket.create_connection(QLC_WS)
    ws.send(f"QLC+API|setFunctionStatus|{qlc_function.value}|255")
    ws.close()


buttons = {}
for pin, func in BUTTON_MAP.items():
    btn = Button(pin, pull_up=True, bounce_time=0.05)
    btn.when_pressed = lambda function=func: fire_qlc_function(function)
    buttons[pin] = btn

print("Macro pad running. Press Ctrl+C to stop.")
while True:
    time.sleep(1)
