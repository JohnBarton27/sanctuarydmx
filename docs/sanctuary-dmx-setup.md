# Sanctuary DMX — Setup & Operations Guide

## Overview

This document covers the setup and operation of the Sanctuary DMX lighting control system, built on a Raspberry Pi 4 running QLC+ 4. The Pi runs headlessly and is controlled via a web browser on any device connected to the same network.

**System summary:**

| Component | Details |
|---|---|
| Hardware | Raspberry Pi 4 |
| OS | Raspberry Pi OS (64-bit, Bookworm) |
| Software | QLC+ 4 |
| Hostname | `sanctuary_dmx` |
| Web interface | `http://sanctuary_dmx.local:9999` |
| SSH user | `pi` |

---

## For Volunteers — Day-to-Day Operation

1. Ensure the Pi is powered on (small black box, red + green LEDs should be lit)
2. Connect your device to the sanctuary Wi-Fi
3. Open a browser and go to `http://sanctuary_dmx.local:9999`
4. The QLC+ virtual console will load automatically in operate mode
5. Use the on-screen controls to run the lighting show

> The Pi may take up to 90 seconds after power-on before the web interface is reachable.

---

## System Architecture

The Pi runs QLC+ as a **systemd service** that starts automatically on boot. It launches in headless mode using the `offscreen` Qt platform plugin, with the web interface enabled on port 9999. A saved project file is loaded automatically at startup.

```
Boot → systemd starts qlcplus.service → QLC+ loads project → web UI available at :9999
```

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
ExecStart=/usr/bin/qlcplus --web --nowm --operate --open /home/pi/show.qxw
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

## Show Design Workflow

QLC+ show design must be done in the full desktop application — the web interface is operate-mode only. The recommended workflow is:

1. SSH into the Pi with X11 forwarding from a laptop on the same network:

```bash
ssh -X pi@sanctuary_dmx.local
```

2. Stop the background service temporarily:

```bash
sudo systemctl stop qlcplus
```

3. Launch QLC+ with a display:

```bash
qlcplus
```

4. Design your show, then **save the project to `/home/pi/show.qxw`**

5. Exit QLC+ and restart the service:

```bash
sudo systemctl start qlcplus
```

The new project will be loaded automatically on the next boot, or immediately via the restart above.

### Transferring a Project from Another Machine

If designing on a separate laptop, copy the project file to the Pi with:

```bash
scp yourshow.qxw pi@sanctuary_dmx.local:/home/pi/show.qxw
```

Then restart the service:

```bash
ssh pi@sanctuary_dmx.local sudo systemctl restart qlcplus
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
