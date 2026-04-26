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
| Physical control | USB macro keypad (16 keys + knob) |

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

The Pi runs two **systemd services** that start automatically on boot:

- **`qlcplus.service`** — runs QLC+ in headless mode with the web interface on port 9999
- **`key_control.service`** — reads the USB macro keypad and sends commands to QLC+ over WebSocket

```
Boot → qlcplus.service → QLC+ loads project → web UI at :9999
                ↑
     key_control.service → reads USB keypad → WebSocket → QLC+
```

---

## Macro Keypad Controls

The keypad provides direct physical control over lighting without needing the web interface. Keys trigger color scenes with a 2-second fade. The top-right knob adjusts master brightness in ~5% steps.

### Color Keys

| Key | Scene |
|-----|-------|
| A | Blackout |
| B | White |
| C | Pink |
| D | Red |
| E | Amber |
| F | Warm White |
| G | Green |
| H | Teal |
| I | Light Blue |
| J | Blue |
| K | Purple |

### Brightness Knob (top-right)

| Action | Effect |
|--------|--------|
| Turn left | Brightness −5% |
| Turn right | Brightness +5% |

Brightness affects both fixtures together and persists across scene changes. It resets to 100% when `key_control.service` restarts.
