from gpiozero import Button
import requests
import time

QLC_BASE = "http://localhost:9999/api"

# Map GPIO pin → QLC+ function ID
BUTTON_MAP = {
    4: 1,   # GPIO4 → QLC function ID 1
}

def fire_qlc_function(func_id):
    print(f"Firing {func_id}")
    # requests.get(f"{QLC_BASE}/functionSetRunning?id={func_id}&running=true")

buttons = {}
for pin, func_id in BUTTON_MAP.items():
    btn = Button(pin, pull_up=True, bounce_time=0.05)
    btn.when_pressed = lambda fid=func_id: fire_qlc_function(fid)
    buttons[pin] = btn

print("Macro pad running. Press Ctrl+C to stop.")
while True:
    time.sleep(1)