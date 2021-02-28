#!/usr/bin/env python3

import argparse
from time import sleep

from src.config import Config

from src.device.device_manager import DeviceManager
from src.fan.fan_controller import FanController

parser = argparse.ArgumentParser(description='display', usage='%(prog)s [-t 50] [-g 15] [-r 3]')

parser.add_argument(
    '-t', '--threshold',
    type=int,
    help='a threshold temperature',
    default=40
)

parser.add_argument(
    '-g', '--grace_period',
    type=int,
    help='number of temperature samples before applying on/off',
    default=Config.fan_default_samples
)

parser.add_argument(
    '-f', '--refresh-interval',
    type=int,
    help='interval between to data sample',
    default=1
)

args = parser.parse_args()

device_manager = DeviceManager(
    fan_controller=FanController(threshold=args.threshold, samples=args.grace_period)
)

device_manager.splash()
sleep(Config.splash_show_time)

device_manager.clear()

try:
    while True:
        device_manager.update()
        sleep(args.refresh_interval)

except KeyboardInterrupt:
    print("ctrl + c:")
    device_manager.stop()
