# Setup Instructions

## Overview

This document covers the setup of the Sanctuary DMX lighting control system, built on a Raspberry Pi 4 running QLC+ 4.

---

## Initial Setup

### 1. Flash the OS

1. Download [Raspberry Pi Imager](https://www.raspberrypi.com/software/)
2. Select **Raspberry Pi 4** as the device
3. Select **Raspberry Pi OS (64-bit)** as the OS
4. Under **Edit Settings**, configure:
   - Hostname: `sanctuary_dmx`
   - Username: `pi`
   - Password: *(your chosen password)*
   - Wi-Fi SSID and password
   - Enable SSH under the Services tab
5. Write to the SD card and **allow the verify step to complete fully**

### 2. First Boot

Insert the SD card and power on the Pi. On first boot, allow up to 90 seconds for initial setup to complete. If the Pi does not appear on the network, connect a monitor and keyboard and run:

```bash
sudo raspi-config
```

From here you can manually configure Wi-Fi, SSH, and hostname under **System Options**.

### 3. Update the System

```bash
sudo apt update && sudo apt upgrade -y
```

### 4. Install QLC+

```bash
sudo apt install qlcplus -y
sudo apt install libqt5websockets5 -y
```

### 5. Create the systemd Service

```bash
sudo tee /etc/systemd/system/qlcplus.service << 'EOF'
[Unit]
Description=QLC+ DMX Controller
After=network.target

[Service]
Environment=QT_QPA_PLATFORM=offscreen
ExecStart=/usr/bin/qlcplus --web --nowm --operate --open /home/pi/Documents/sanctuarydmx/sanctuary_lights.qxw
Restart=on-failure
RestartSec=5
User=pi

[Install]
WantedBy=multi-user.target
EOF
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable qlcplus
sudo systemctl start qlcplus
```

> Update the `--open` path to match the actual project filename once a show has been created.

### 6. Set Up the Macro Keypad Controller

The `key_control` script reads the USB macro keypad and sends lighting commands to QLC+ over WebSocket.

**Deploy the files:**

```bash
scp -r key_control pi@sanctuary_dmx.local:/home/pi/Documents/sanctuarydmx/
```

**Create a Python virtual environment and install dependencies:**

```bash
ssh pi@sanctuary_dmx.local
cd /home/pi/Documents/sanctuarydmx/key_control
python3 -m venv venv
venv/bin/pip install -r requirements.txt
```

**Allow the `pi` user to read input devices:**

```bash
sudo usermod -aG input pi
```

Log out and back in (or reboot) for the group change to take effect.

**Install and enable the service:**

```bash
sudo cp /home/pi/Documents/sanctuarydmx/setup/key_control.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable key_control
sudo systemctl start key_control
```

**Verify it's running:**

```bash
sudo systemctl status key_control
```

---

## Network Configuration

The Pi is configured to connect to the sanctuary Wi-Fi automatically. To add or update a network:

```bash
sudo nmtui
```

Select **Edit a connection → Add → Wi-Fi** and enter the network credentials.

### Accessing the Pi by IP Address

If `sanctuary_dmx.local` does not resolve on your device, find the Pi's IP address from your router's DHCP client list, or by running on the Pi:

```bash
hostname -I
```

Then access the web interface at `http://<ip-address>:9999`.

---

## Maintenance

### Check Service Status

```bash
sudo systemctl status qlcplus
```

### Restart QLC+

```bash
sudo systemctl restart qlcplus
```

### View Logs

```bash
journalctl -u qlcplus -n 50
```

### Reboot the Pi

```bash
sudo reboot
```

---

## Troubleshooting

| Symptom | Likely cause | Resolution |
|---|---|---|
| Solid red LED, no green | Not booting from SD card | Reflash SD card, ensure verify step completes |
| Green LED flashes then stops | First-run config error | Check cloud-init config files on `bootfs` partition |
| Web interface unreachable | Service not running, or Pi still booting | Wait 90 seconds; check `systemctl status qlcplus` |
| Virtual console unresponsive | QLC+ in design mode | Ensure `--operate` flag is in the service `ExecStart` line |
| Can't SSH in | SSH not enabled, or wrong hostname | Connect monitor/keyboard and run `sudo raspi-config` |
| Keypad has no effect | `key_control` service not running | Check `systemctl status key_control`; check `journalctl -u key_control -n 50` |
| Keypad device not found | Keypad unplugged, or wrong device name | Confirm USB connection; run `python main.py --list-devices` to verify device name |
| Permission denied on `/dev/input` | `pi` user not in `input` group | Run `sudo usermod -aG input pi` and reboot |
