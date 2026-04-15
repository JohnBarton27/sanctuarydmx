from enum import Enum
from gpiozero import Button
import requests
import time

QLC_BASE = "http://localhost:9999/api"


class QlcFunctions(Enum):
    BLACKOUT = 1


# Map GPIO pin → QLC+ function ID
BUTTON_MAP = {
    4: QlcFunctions.BLACKOUT,   # GPIO4 → QLC function ID 1
}


def fire_qlc_function(qlc_function):
    print(f"Firing {qlc_function}")
    # requests.get(f"{QLC_BASE}/functionSetRunning?id={func_id}&running=true")


buttons = {}
for pin, func in BUTTON_MAP.items():
    btn = Button(pin, pull_up=True, bounce_time=0.05)
    btn.when_pressed = lambda function=func: fire_qlc_function(function)
    buttons[pin] = btn

print("Macro pad running. Press Ctrl+C to stop.")
while True:
    time.sleep(1)
