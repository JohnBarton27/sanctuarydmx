# Wiki Setup Guide

## Overview

The Sanctuary DMX wiki runs on MkDocs, a static site generator that reads plain Markdown files directly from disk. It is served by the Pi as a systemd service alongside QLC+ and is accessible from any device on the same network.

**Wiki summary:**

| Component | Details |
|---|---|
| Software | MkDocs |
| Web interface | `http://sanctuary_dmx.local:8000` |
| Service name | `mkdocs` |
| Project root | `~/wiki/` |
| Config file | `~/wiki/mkdocs.yml` |
| Content files | `~/wiki/docs/*.md` |

---

## Repository Structure

```
wiki/
├── mkdocs.yml        # Site configuration — navigation, theme, extensions
└── docs/
    ├── index.md      # Home page
    ├── sanctuary-dmx-setup.md
    └── wiki-setup.md
```

All documentation lives in `docs/` as plain `.md` files. The `mkdocs.yml` file
at the repo root controls the site title, navigation sidebar, and theme.

---

## Adding or Editing Pages

### From your laptop (recommended)

1. Write or edit a `.md` file locally
2. Copy it to the Pi:

    ```
    scp yourpage.md pi@sanctuary_dmx.local:/home/pi/wiki/docs/
    ```

3. Register it in `mkdocs.yml` under the `nav` section:

    ```
    nav:
      - Home: index.md
      - Setup & Operations: sanctuary-dmx-setup.md
      - Wiki Setup: wiki-setup.md
      - Your New Page: yourpage.md
    ```

4. Copy the updated `mkdocs.yml` to the Pi:

    ```
    scp mkdocs.yml pi@sanctuary_dmx.local:/home/pi/wiki/
    ```

MkDocs picks up changes automatically — no restart required.

### Directly on the Pi via SSH

```bash
ssh pi@sanctuary_dmx.local
nano ~/wiki/docs/yourpage.md
```

Then update `mkdocs.yml` if adding a new page:

```bash
nano ~/wiki/mkdocs.yml
```

---

## systemd Service

MkDocs runs as a systemd service and starts automatically on boot.

### Service file location
`/etc/systemd/system/mkdocs.service`

```ini
[Unit]
Description=MkDocs Wiki
After=network.target

[Service]
ExecStart=/usr/bin/mkdocs serve --dev-addr=0.0.0.0:8000
WorkingDirectory=/home/pi/wiki
Restart=on-failure
RestartSec=5
User=pi

[Install]
WantedBy=multi-user.target
```

### Useful commands

```bash
sudo systemctl status mkdocs      # Check if running
sudo systemctl restart mkdocs     # Restart the service
sudo systemctl stop mkdocs        # Stop the service
journalctl -u mkdocs -n 50        # View logs
```

---

## Initial Setup

If setting up from scratch on a new Pi:

### 1. Install MkDocs

```bash
sudo apt install mkdocs -y
```

### 2. Clone or recreate the wiki repo

```bash
cd ~
mkdocs new wiki
cd ~/wiki
git init
git config user.email "sanctuary@local"
git config user.name "Sanctuary DMX"
```

### 3. Copy in content files and mkdocs.yml from the repo

```bash
scp -r docs/ mkdocs.yml pi@sanctuary_dmx.local:/home/pi/wiki/
```

### 4. Create the systemd service

```bash
sudo tee /etc/systemd/system/mkdocs.service << 'EOF'
[Unit]
Description=MkDocs Wiki
After=network.target

[Service]
ExecStart=/usr/bin/mkdocs serve --dev-addr=0.0.0.0:8000
WorkingDirectory=/home/pi/wiki
Restart=on-failure
RestartSec=5
User=pi

[Install]
WantedBy=multi-user.target
EOF
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable mkdocs
sudo systemctl start mkdocs
```

### 5. Verify

Open `http://sanctuary_dmx.local:8000` in a browser. The wiki should load with
the navigation sidebar populated from `mkdocs.yml`.