from PIL import Image, ImageDraw, ImageFont

from src.constants import FONT_FILE
from src.fan.data_collector import DataCollector


class StatLine:
    def __init__(self, collector: DataCollector, formatter, foreground_color, font_size, width):
        self._collector = collector
        self._formatter = formatter
        self._foreground_color = foreground_color
        self._font_size = font_size
        self._width = width
        self._height = self._font_size + 4
        self._font = ImageFont.truetype(FONT_FILE, self._font_size)

    def draw(self):
        image = Image.new('RGB', (self._width, self._height))
        draw = ImageDraw.Draw(image)

        draw.text(
            (4, 1),
            self._formatter(self._collector),
            fill=self._foreground_color,
            font=self._font
        )

        return image

    def height(self):
        return self._height
