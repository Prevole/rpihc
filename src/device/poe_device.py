import smbus

import os

from lib.waveshare.ssd1306 import SSD1306, ClearColor
from src.data.base_data import BaseData
from src.data.oberserver import Observer
from src.data.poller import Histos, HistoType
from src.fan.fan_controller import FanController
from src.oled.oled_drawer import OledDrawer

DISPLAY = SSD1306()
DISPLAY.init()
dir_path = os.path.dirname(os.path.abspath(__file__))


class PoEDevice(Observer):
    def __init__(self, fan_controller: FanController, is_reverse=False, address=0x20):
        self._i2c = smbus.SMBus(1)
        self._address = address
        self._is_reverse = is_reverse
        self._drawer = OledDrawer(
            width=DISPLAY.width,
            height=DISPLAY.height
        )
        self._fan_control = fan_controller

    @staticmethod
    def clear():
        DISPLAY.clear(color=ClearColor.BLACK)

    def notify(self, data: BaseData, histos: Histos):
        image = self._drawer.draw(
            ip=data.ip(),
            temperature=histos.histo(HistoType.TEMPERATURE).current(),
            fan_mode=self._fan_control.mode()
        )

        if self._is_reverse:
            DISPLAY.show_image(DISPLAY.get_buffer(image.rotate(180)))
        else:
            DISPLAY.show_image(DISPLAY.get_buffer(image))

        if self._fan_control.has_changed():
            self._i2c.write_byte(self._address, self._fan_control.mode().op(self._i2c.read_byte(self._address)))
