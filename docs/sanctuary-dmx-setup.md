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
ExecStart=/usr/bin/qlcplus --web --nowm --operate --open /home/pi/Documents/sanctuary_lights.qxw
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
