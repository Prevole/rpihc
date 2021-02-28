import os

from PIL import ImageFont

from src.config import Config


FONT_LCD_NORMAL = ImageFont.truetype(Config.font_file_bold, Config.lcd_histo_font_size_normal)
FONT_LCD_SMALL = ImageFont.truetype(Config.font_file_bold, Config.lcd_histo_font_size_small)

FONT_OLED_NORMAL = ImageFont.truetype(Config.font_file_normal, Config.oled_font_size_normal)
FONT_OLED_SMALL = ImageFont.truetype(Config.font_file_normal, Config.oled_font_size_small)
