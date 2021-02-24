# Raspberry Pi 4 - Hardware Control

## WaveShare PoE HAT Display (SSD1306)

The script `bin/poehat.py` will show:

* `IP` address
* `CPU Temperature`
* PoE HAT `FAN` status (On/Off)

The script is configurable to start the `FAN` when a threshold temperature is over.

To run the script:

```bash
bin/poehat.py 45
```