import os

from PIL import Image, ImageDraw, ImageFont

from src.poe_hat.data_collector import DataCollector
from src.poe_hat.fan_control import FanControl

DIR_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../resources'))

FONT_FILE = f'{DIR_PATH}/Courier_New.ttf'
FONT_NORMAL = ImageFont.truetype(FONT_FILE, 13)
FONT_SMALL = ImageFont.truetype(FONT_FILE, 12)


class PoEHatImageDrawer:
    def __init__(self, width, height, data_collector: DataCollector, fan_control: FanControl):
        self._width = width
        self._height = height
        self._data_collector = data_collector
        self._fan_control = fan_control

    def draw(self):
        image = Image.new('1', (self._width, self._height), 'WHITE')
        draw = ImageDraw.Draw(image)

        draw.text((0, 1), f'IP:{self._data_collector.ip()}', font=FONT_NORMAL, fill=0)
        draw.text((0, 15), f'Temp:{self._data_collector.temperature()}', font=FONT_NORMAL, fill=0)
        draw.text((77, 16), f'FAN:{self._fan_control.mode().text}', font=FONT_SMALL, fill=0)

        return image
