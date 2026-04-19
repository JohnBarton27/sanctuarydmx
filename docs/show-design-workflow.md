# Show Design Workflow

QLC+ show design must be done in the full desktop application — the web interface is operate-mode only. The recommended workflow is:

1. SSH into the Pi with X11 forwarding from a laptop on the same network:

    ```
    ssh -X pi@sanctuary_dmx.local
    ```

2. Stop the background service temporarily:

    ```
    sudo systemctl stop qlcplus
    ```

3. Launch QLC+ with a display:

    ```
    qlcplus
    ```

4. Design your show, then **save the project to `/home/pi/Documents/sanctuarydmx/sanctuary_lights.qxw`**

5. Exit QLC+ and restart the service:

    ```
    sudo systemctl start qlcplus
    ```

The new project will be loaded automatically on the next boot, or immediately via the restart above.

## Transferring a Project from Another Machine

If designing on a separate laptop, copy the project file to the Pi with:

```bash
scp yourshow.qxw pi@sanctuary_dmx.local:/home/pi/Documents/sanctuarydmx/sanctuary_lights.qxw
```

Then restart the service:

```bash
ssh pi@sanctuary_dmx.local sudo systemctl restart qlcplus
```

---