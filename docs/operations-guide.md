# Operations Guide

## Overview

This document covers the operation of the Sanctuary DMX lighting control system. The Pi runs headlessly and is controlled via a web browser on any device connected to the same network.

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
