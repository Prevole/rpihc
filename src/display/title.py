from PIL import Image, ImageDraw, ImageFont

from src.config import Config

from src.data.base_data import BaseData
from src.data.oberserver import Observer


class Title(Observer):
    def __init__(self, background_color, foreground_color, font_size, width):
        self._background_color = background_color
        self._foreground_color = foreground_color
        self._font_size = font_size
        self._width = width
        self._height = self._font_size + 8
        self._font = ImageFont.truetype(Config.font_file_bold, self._font_size)

    def draw(self, data: BaseData):
        image = Image.new('RGB', (self._width, self._height), self._background_color)
        draw = ImageDraw.Draw(image)

        draw.text((4, 3), f'{data.hostname()} / {data.ip()}', fill=self._foreground_color, font=self._font)

        return image

    def height(self):
        return self._height
