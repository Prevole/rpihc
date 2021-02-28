# Raspberry Pi 4 - Hardware Control

## One Script to Rule Them All

The script `bin/display.py` will show:

* `IP` address
* `CPU Temperature`
* PoE HAT `FAN` status (On/Off)

on a small Waveshare PoE HAT OLDE Display (SSD1306)

On a LCD 2.4 inch screen, it will show: `memory`, `cpu` and `temperature`. The `hostname` and `ip` are also shown.

## To run the script

To run the script:

```bash
bin/display.py [-t 50] [-g 15] [-r 3]
```