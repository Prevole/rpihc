import math

from PIL import Image, ImageDraw

from src.config import Config
from src.constants import FONT_LCD_NORMAL, FONT_LCD_SMALL
from src.data.poller import Histo
from src.data.threshold import ThresholdConfiguration
from src.display.histo_drawer import HistoDrawer


class HistoPaneDrawer:
    def __init__(self, name, label_factory, width, height, size, threshold_config: ThresholdConfiguration):
        self._name = name
        self._label_factory = label_factory
        self._width = width
        self._height = height
        self._histo_drawer = HistoDrawer(math.ceil(width / 3 * 2), math.ceil(height / 3 * 2), size, threshold_config)
        self._histo_position = (math.ceil(width / 3), 0)
        self._name_position = (0, math.ceil(height / 2) - math.ceil(FONT_LCD_NORMAL.size / 2))
        self._label_position = (math.ceil(width / 8), math.ceil(height / 3 * 2))

    def draw(self, histo: Histo):
        image = Image.new('RGB', (self._width, self._height))
        draw = ImageDraw.Draw(image)

        image.paste(self._histo_drawer.draw(histo), self._histo_position)

        draw.text(self._name_position, self._name, fill=Config.lcd_histo_color_fg, font=FONT_LCD_NORMAL)
        draw.text(self._label_position, self._label_factory(histo), fill=Config.lcd_histo_color_fg, font=FONT_LCD_SMALL)

        return image

    def height(self):
        return self._height
