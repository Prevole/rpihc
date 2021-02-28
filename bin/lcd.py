#!/usr/bin/env python3

import os
import sys
import time
import logging

from psutil._common import bytes2human

from src.data.histo_stack import HistoStack
from src.data.poller import Poller
from src.data.threshold import ThresholdConfiguration
from src.display.histo_drawer import HistoDrawer
# from src.data.histo_stack import HistoStack
from lib.waveshare.lcd.display import Display
from src.display.histo_pane_drawer import HistoPaneDrawer
from src.display.stat_line import StatLine
from src.display.title import Title
from src.poe_hat.data_collector import DataCollector

sys.path.append("..")
from PIL import Image, ImageDraw, ImageFont

DIR_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../resources'))
IMG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '../resources/img.jpg'))

FONT_FILE = f'{DIR_PATH}/Courier_New.ttf'
FONT_NORMAL = ImageFont.truetype(FONT_FILE, 13)
FONT_SMALL = ImageFont.truetype(FONT_FILE, 10)

# Raspberry Pi pin configuration:
RST = 27
DC = 25
BL = 18
bus = 0 
device = 0 
logging.basicConfig(level=logging.DEBUG)
try:
    # display with hardware SPI:
    ''' Warning!!!Don't  creation of multiple displayer objects!!! '''
    #disp = LCD_2inch4.LCD_2inch4(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)
    disp = Display()

    # Initialize library.
    disp.init()

    # Clear display.
    disp.clear()

    # Create blank image for drawing.
    image1 = Image.new("RGB", (disp.height, disp.width), "BLACK")
    draw = ImageDraw.Draw(image1)

    # stack = HistoStack(10, 10)

    collector = DataCollector()
    poller = Poller(collector=collector)

    # mem_drawer = HistoDrawer(100, 20, poller.memory_stack())
    # cpu_drawer = HistoDrawer(100, 20, poller.cpu_stack())

    # for value in [2, 4, 6, 8, 10, 9, 7, 5, 3, 1, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
    #     stack.add(value)
    #     image1.paste(drawer.draw(), (10, 10))
    #     disp.show_image(image1)
    #     time.sleep(0.5)

    def memory_label(stack: HistoStack):
        total = bytes2human(stack.max())
        current = bytes2human(stack.current())

        return f'{current} / {total}'

    def cpu_label(stack: HistoStack):
        return f'{stack.current()}%'

    def temp_label(stack: HistoStack):
        return f'{stack.current()}°'

    title = Title(
        collector=collector,
        background_color='#0000FF',
        foreground_color='#FFFFFF',
        font_size=15,
        width=disp.height - 5
    )

    space_size = 2

    image1.paste(title.draw(), (0, 0))

    memory_pane = HistoPaneDrawer(
        name='Mem:',
        stack=poller.memory_stack(),
        label_factory=memory_label,
        width=150,
        height=40,
        threshold_config=ThresholdConfiguration(default_color='#00FF00').complete()
    )

    cpu_pane = HistoPaneDrawer(
        name='CPU:',
        stack=poller.cpu_stack(),
        label_factory=cpu_label,
        width=150,
        height=40,
        threshold_config=ThresholdConfiguration(default_color='#00FF00')
            .add(40, '#00FF00')
            .add(50, '#FFA500')
            .add(100, '#FF0000')
            .complete()
    )

    temp_pane = HistoPaneDrawer(
        name='Temp:',
        stack=poller.temp_stack(),
        label_factory=temp_label,
        width=150,
        height=40,
        threshold_config=ThresholdConfiguration(default_color='#00FF00')
            .add(30, '#00FF00')
            .add(40, '#FFFF00')
            .add(50, '#FFA500')
            .add(100, '#FF0000')
            .complete()
    )

    # temp_line = StatLine(collector=collector, formatter=temp_formatter, foreground_color='#00FF00', font_size=12, width=140)

    while True:
        poller.update()
        # disp.clear()
        # image1.paste(mem_drawer.draw(), (10, 10))

        # draw.text((10, 40), f'{current} / {total}', fill="WHITE", font=FONT_SMALL)

        # image1.paste(cpu_drawer.draw(), (10, 60))

        image1.paste(memory_pane.draw(), (0, title.height() + space_size))
        image1.paste(cpu_pane.draw(), (0, title.height() + memory_pane.height() + (2 * space_size)))
        image1.paste(temp_pane.draw(), (165, title.height() + space_size))

        image1.rotate(90)

        disp.show_image(image1)
        time.sleep(1)

    disp.clear()
    disp.module_exit()
    exit()

    # logging.info("draw point")

    # draw.rectangle((5,10,6,11), fill = "BLACK")
    # draw.rectangle((5,25,7,27), fill = "BLACK")
    # draw.rectangle((5,40,8,43), fill = "BLACK")
    # draw.rectangle((5,55,9,59), fill = "BLACK")
    #
    # logging.info("draw line")
    # draw.line([(20, 10),(70, 60)], fill = "RED",width = 1)
    # draw.line([(70, 10),(20, 60)], fill = "RED",width = 1)
    # draw.line([(170,15),(170,55)], fill = "RED",width = 1)
    # draw.line([(150,35),(190,35)], fill = "RED",width = 1)
    #
    # logging.info("draw rectangle")
    # draw.rectangle([(20,10),(70,60)],fill = "WHITE",outline="BLUE")
    # draw.rectangle([(85,10),(130,60)],fill = "BLUE")
    #
    # logging.info("draw circle")
    # draw.arc((150,15,190,55),0, 360, fill =(0,255,0))
    # draw.ellipse((150,65,190,105), fill = (0,255,0))
    #
    # logging.info("draw text")
    # # Font1 = ImageFont.truetype("../Font/Font01.ttf",25)
    # # Font2 = ImageFont.truetype("../Font/Font01.ttf",35)
    # # Font3 = ImageFont.truetype("../Font/Font02.ttf",32)
    #
    # draw.rectangle([(0,65),(140,100)],fill = "WHITE")
    # draw.text((5, 68), 'Hello world', fill = "BLACK",font=FONT_NORMAL)
    # draw.rectangle([(0,115),(190,160)],fill = "RED")
    # draw.text((5, 118), 'WaveShare', fill = "WHITE",font=FONT_NORMAL)
    # draw.text((5, 160), '1234567890', fill = "GREEN",font=FONT_NORMAL)
    # text= u"微雪电子"
    # draw.text((5, 200),text, fill = "BLUE",font=FONT_NORMAL)
    # image1=image1.rotate(0)
    # disp.show_image(image1)
    # time.sleep(3)
    # logging.info("show image")
    # image = Image.open(IMG_FILE)
    # image = image.rotate(0)
    # disp.show_image(image)
    # time.sleep(3)
    # disp.module_exit()
    # logging.info("quit:")
except IOError as e:
    logging.info(e)    
except KeyboardInterrupt:
    disp.module_exit()
    logging.info("quit:")
    exit()