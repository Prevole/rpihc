import smbus

import os

from lib.waveshare.ssd1306 import SSD1306, ClearColor
from src.poe_hat.fan_control import FanControl
from src.poe_hat.image_drawer import PoEHatImageDrawer

DISPLAY = SSD1306()
DISPLAY.init()
dir_path = os.path.dirname(os.path.abspath(__file__))


class PoEHatDevice:
    def __init__(self, drawer: PoEHatImageDrawer, fan_control: FanControl, is_reverse=False, address=0x20):
        self._i2c = smbus.SMBus(1)
        self._address = address
        self._is_reverse = is_reverse
        self._drawer = drawer
        self._fan_control = fan_control

    def update_fan(self):
        self._i2c.write_byte(self._address, self._fan_control.mode().op(self._i2c.read_byte(self._address)))

    @staticmethod
    def clear():
        DISPLAY.clear(color=ClearColor.BLACK)

    def display(self):
        image = self._drawer.draw()

        if self._is_reverse:
            DISPLAY.show_image(DISPLAY.get_buffer(image.rotate(180)))
        else:
            DISPLAY.show_image(DISPLAY.get_buffer(image))
