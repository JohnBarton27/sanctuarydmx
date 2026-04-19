# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Sanctuary DMX is a lighting control system for a church sanctuary. A Raspberry Pi 4 runs [QLC+](https://www.qlcplus.org/) headlessly as a systemd service, exposing a web UI on port 9999. A Python script (`key_control/main.py`) listens to physical GPIO buttons and triggers QLC+ lighting functions over WebSocket.

## Architecture

```
Boot → systemd (qlcplus.service) → QLC+ loads sanctuary_lights.qxw → web UI at :9999
GPIO buttons → key_control/main.py → WebSocket (ws://localhost:9999/qlcplusWS) → QLC+ functions
```

- **`key_control/main.py`** — Runs on the Pi. Maps GPIO pins to `QlcFunctions` enum values and fires them via the QLC+ WebSocket API using the message format `QLC+API|setFunctionStatus|<id>|<value>`.
- **`key_control/requirements.txt`** — Only dependency is `websocket-client`. `gpiozero` is available on Raspberry Pi OS by default.
- **`setup/`** — Contains systemd unit files for `qlcplus.service` and `mkdocs.service`.
- **`docs/`** — MkDocs source for the operations and setup wiki, served by `mkdocs.service`.

## Key Control Script

The `BUTTON_MAP` dict in `main.py` maps GPIO pin numbers to `QlcFunctions` enum members. The enum values are QLC+ function IDs — these must match the function IDs assigned inside the `.qxw` project file. To add a new button, add an entry to `BUTTON_MAP` and ensure the corresponding function exists in QLC+.

WebSocket message format: `QLC+API|setFunctionStatus|{function_id}|{value}` where value 255 = on, 0 = off.

## Running the Key Control Script

```bash
cd key_control
pip install -r requirements.txt
python main.py
```

This must run on the Pi (requires GPIO hardware). Deploy by copying to the Pi and running under a systemd service or manually.

## Docs (MkDocs)

```bash
pip install mkdocs mkdocs-readthedocs
mkdocs serve        # local preview at http://127.0.0.1:8000
mkdocs build        # build static site to site/
```

## Deployment Notes

- QLC+ project file lives at `/home/pi/Documents/sanctuary_lights.qxw` on the Pi
- Show design must be done in the full desktop app (not the web UI); use SSH X11 forwarding: `ssh -X pi@sanctuary_dmx.local`
- Stop the service before designing: `sudo systemctl stop qlcplus`, restart after: `sudo systemctl start qlcplus`
- Transfer a project file: `scp yourshow.qxw pi@sanctuary_dmx.local:/home/pi/Documents/sanctuary_lights.qxw`
- Web UI: `http://sanctuary_dmx.local:9999`
