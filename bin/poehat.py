#!/usr/bin/env python3

import argparse
import time

from lib.waveshare.ssd1306 import ClearColor
from src.poe_hat.data_collector import DataCollector
from src.poe_hat.fan_control import FanControl
from src.poe_hat.image_drawer import PoEHatImageDrawer
from src.poe_hat.poe_hat_device import PoEHatDevice, DISPLAY

parser = argparse.ArgumentParser(description='PoEHat')
parser.add_argument('threshold', type=int, help='a threshold temperature', default=45)

args = parser.parse_args()

data_collector = DataCollector()
fan_control = FanControl(threshold=args.threshold, data_collector=data_collector)
drawer = PoEHatImageDrawer(width=DISPLAY.width, height=DISPLAY.height, data_collector=data_collector, fan_control=fan_control)
device = PoEHatDevice(drawer=drawer, fan_control=fan_control, is_reverse=True)

device.clear()

try:
    while 1:
        fan_control.update()
        device.update_fan()
        device.display()
        time.sleep(1)

except KeyboardInterrupt:
    print("ctrl + c:")
    fan_control.force_on()
    device.update_fan()
    device.clear()
