#!/usr/bin/env python3

import argparse
import time

from src.poe_hat.data_collector import DataCollector
from src.poe_hat.fan_control import FanControl
from src.poe_hat.image_drawer import PoEHatImageDrawer
from src.poe_hat.poe_hat_device import PoEHatDevice, DISPLAY

parser = argparse.ArgumentParser(description='PoEHat', usage='%(prog)s [-t 50] [-g 15] [-d 3]')

parser.add_argument(
    '-t', '--threshold',
    type=int,
    help='a threshold temperature',
    default=45
)

parser.add_argument(
    '-g', '--grace_period',
    type=int,
    help='number of temperature samples before applying on/off',
    default=10
)

parser.add_argument(
    '-d', '--delay',
    type=int,
    help='delay in seconds between two temperature samples',
    default=1
)

args = parser.parse_args()

data_collector = DataCollector()
fan_control = FanControl(threshold=args.threshold, samples=args.grace_period, data_collector=data_collector)
drawer = PoEHatImageDrawer(
    width=DISPLAY._width,
    height=DISPLAY._height,
    data_collector=data_collector,
    fan_control=fan_control
)
device = PoEHatDevice(drawer=drawer, fan_control=fan_control, is_reverse=True)

device.clear()

try:
    while 1:
        fan_control.update()
        device.update_fan()
        device.display()
        time.sleep(args.delay)

except KeyboardInterrupt:
    print("ctrl + c:")
    fan_control.force_on()
    device.update_fan()
    device.clear()
