import math

from PIL import Image, ImageDraw

from src.data.poller import Histo
from src.data.threshold import ThresholdConfiguration


class HistoDrawer:
    def __init__(self, width, height, size, threshold_config: ThresholdConfiguration):
        self._width = width
        self._height = height
        self._threshold_config = threshold_config
        self._bar_width = self._width / size
        self._unit_height = self._height / threshold_config.max()

    def draw(self, histo: Histo):
        image = Image.new('RGB', (self._width, self._height))
        draw = ImageDraw.Draw(image)

        for idx, value in enumerate(histo.values()):
            if value > -1:
                x0 = idx * self._bar_width
                x1 = x0 + self._bar_width
                y0 = 0
                y1 = math.ceil(self._unit_height * value)
                draw.rectangle((x0, y0, x1, y1), fill=self._threshold_config.match(value).color())

        return image.transpose(Image.FLIP_TOP_BOTTOM)
