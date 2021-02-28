import os

from PIL import Image
from psutil._common import bytes2human

from lib.waveshare.lcd.display import Display

from src.config import Config
from src.data.base_data import BaseData
from src.data.oberserver import Observer
from src.data.poller import Histos, Histo, HistoType
from src.display.histo_pane_drawer import HistoPaneDrawer
from src.display.title import Title

# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0
device = 0

IMG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../resources/darknest-rpi-logo.png'))

spacer = 2


def memory_label(histo: Histo):
    total = bytes2human(histo.max())
    current = bytes2human(histo.current())

    return f'{current} / {total}'


def cpu_label(histo: Histo):
    return f'{histo.current()}%'


def temperature_label(histo: Histo):
    return f'{histo.current()}°'


def create_title(width):
    return Title(
        background_color=Config.lcd_title_color_bg,
        foreground_color=Config.lcd_title_color_fg,
        font_size=Config.lcd_title_font_size,
        width=width - 4
    )


def create_histo_pane(name, label_factory, threshold_config):
    return HistoPaneDrawer(
        name=f'{name}:',
        label_factory=label_factory,
        width=Config.lcd_histo_pane_width,
        height=Config.lcd_histo_pane_height,
        size=Config.lcd_histo_samples,
        threshold_config=threshold_config
    )


class LCDDisplay(Observer):
    def __init__(self):
        self._display = Display()

        # Initialize library.
        self._display.init()

        # Clear display.
        self._display.clear()

        self._title = create_title(self._display.height)

        self._histo_cpu = create_histo_pane(
            name='CPU',
            label_factory=cpu_label,
            threshold_config=Config.lcd_histo_threshold_cpu
        )

        self._histo_memory = create_histo_pane(
            name='Mem',
            label_factory=memory_label,
            threshold_config=Config.lcd_histo_threshold_memory
        )

        self._histo_temperature = create_histo_pane(
            name='Temp',
            label_factory=temperature_label,
            threshold_config=Config.lcd_histo_threshold_temperature
        )

    def notify(self, data: BaseData, histos: Histos):
        image = Image.new('RGB', (self._display.height, self._display.width), Config.lcd_color_bg)

        image.paste(self._title.draw(data), (0, 0))

        image.paste(
            im=self._histo_cpu.draw(histos.histo(HistoType.CPU)),
            box=(0, self._title.height() + spacer)
        )

        image.paste(
            im=self._histo_memory.draw(histos.histo(HistoType.MEMORY)),
            box=(0, self._title.height() + Config.lcd_histo_pane_height + (2 * spacer))
        )

        image.paste(
            im=self._histo_temperature.draw(histos.histo(HistoType.TEMPERATURE)),
            box=(0, self._title.height() + (2 * (Config.lcd_histo_pane_height + spacer)))
        )

        self._display.show_image(image)

    def clear(self):
        self._display.clear()

    def splash(self):
        with Image.open(IMG_FILE) as image:
            image = image.rotate(0)
            self._display.show_image(image)
