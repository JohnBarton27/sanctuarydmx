# Sanctuary DMX

Lighting control system for the sanctuary, built on a Raspberry Pi 4 running [QLC+](https://www.qlcplus.org/) 4.

## How It Works

The Pi runs QLC+ headlessly as a systemd service, loading a saved show project on boot. Volunteers control the lights from any browser on the sanctuary Wi-Fi at **`http://sanctuary_dmx.local:9999`**.

A Python script (`key_control/main.py`) listens to physical GPIO buttons wired to the Pi and triggers QLC+ lighting functions over its WebSocket API — no browser needed for button-based control.

```
Boot → systemd starts qlcplus.service → QLC+ loads project → web UI available at :9999
GPIO buttons → key_control/main.py → WebSocket → QLC+ functions
```

## Components

| Component | Details |
|---|---|
| Hardware | Raspberry Pi 4 |
| OS | Raspberry Pi OS 64-bit (Bookworm) |
| Lighting software | QLC+ 4 |
| Button control | Python + gpiozero + websocket-client |
| Documentation | MkDocs |

## Documentation

Full setup, operations, and show design guides are in [`docs/`](docs/) and served as a MkDocs wiki.

- [Setup Instructions](docs/sanctuary-dmx-setup.md)
- [Operations Guide](docs/operations-guide.md)
- [Show Design Workflow](docs/show-design-workflow.md)

## Quick Start

**Day-to-day use:** Power on the Pi, connect to sanctuary Wi-Fi, open `http://sanctuary_dmx.local:9999`.

**Adding a GPIO button:** Edit `BUTTON_MAP` in `key_control/main.py`, mapping a GPIO pin number to a `QlcFunctions` enum value that matches the function ID in your QLC+ project.

**Designing a show:** See [Show Design Workflow](docs/show-design-workflow.md) — design must be done in the desktop app via SSH X11 forwarding, not the web UI.
