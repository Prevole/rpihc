from PIL import Image, ImageDraw

from src.config import Config
from src.constants import FONT_OLED_NORMAL, FONT_OLED_SMALL
from src.fan.fan_controller import FanMode


class OledDrawer:
    def __init__(self, width, height):
        self._width = width
        self._height = height

    def draw(self, ip, temperature, fan_mode: FanMode):
        image = Image.new('1', (self._width, self._height), Config.oled_font_color)
        draw = ImageDraw.Draw(image)

        draw.text((0, 1), f'IP: {ip}', font=FONT_OLED_NORMAL, fill=0)
        draw.text((0, 15), f'Temp: {temperature}°', font=FONT_OLED_NORMAL, fill=0)
        draw.text((80, 15), f'FAN: {fan_mode.text.upper()}', font=FONT_OLED_SMALL, fill=0)

        return image
