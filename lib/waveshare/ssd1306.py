# /*****************************************************************************
# * | File        :	  SSD1306.py
# * | Author      :   Waveshare team
# * | Function    :   SSD1306
# * | Info        :
# *----------------
# * | This version:   V1.0
# * | Date        :   2019-11-14
# * | Info        :
# ******************************************************************************/
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
from enum import Enum

from smbus import SMBus


class ClearColor(Enum):
    WHITE = 0xff
    BLACK = 0x00

    def __init__(self, color):
        self.color = color


class SSD1306(object):
    def __init__(self, width=128, height=32, addr=0x3c):
        self.width = width
        self.height = height
        self.column = width
        self.page = int(height / 8)
        self.addr = addr
        self.bus = SMBus(1)

    def send_command(self, cmd):  # write command
        self.bus.write_byte_data(self.addr, 0x00, cmd)

    def send_data(self, cmd):  # write ram
        self.bus.write_byte_data(self.addr, 0x40, cmd)

    def close_bus(self):
        self.bus.close()

    def init(self):
        self.send_command(0xAE)

        self.send_command(0x40)  # set low column address
        self.send_command(0xB0)  # set high column address

        self.send_command(0xC8)  # not offset

        self.send_command(0x81)
        self.send_command(0xff)

        self.send_command(0xa1)

        self.send_command(0xa6)

        self.send_command(0xa8)
        self.send_command(0x1f)

        self.send_command(0xd3)
        self.send_command(0x00)

        self.send_command(0xd5)
        self.send_command(0xf0)

        self.send_command(0xd9)
        self.send_command(0x22)

        self.send_command(0xda)
        self.send_command(0x02)

        self.send_command(0xdb)
        self.send_command(0x49)

        self.send_command(0x8d)
        self.send_command(0x14)

        self.send_command(0xaf)

    def clear(self, color: ClearColor = ClearColor.WHITE):
        for i in range(0, self.page):
            self.send_command(0xb0 + i)
            self.send_command(0x00)
            self.send_command(0x10)
            for j in range(0, self.column):
                self.send_data(color.color)

    def get_buffer(self, image):
        buf = [0xff] * (self.page * self.column)
        image_monocolor = image.convert('1')
        imwidth, imheight = image_monocolor.size
        pixels = image_monocolor.load()

        if imwidth == self.width and imheight == self.height:
            # print ("Horizontal screen")
            for y in range(imheight):
                for x in range(imwidth):
                    # Set the bits for the column of pixels at the current position.
                    if pixels[x, y] == 0:
                        buf[x + int(y / 8) * self.width] &= ~(1 << (y % 8))

        elif imwidth == self.height and imheight == self.width:
            # print ("Vertical screen")
            for y in range(imheight):
                for x in range(imwidth):
                    newx = y
                    newy = self.height - x - 1
                    if pixels[x, y] == 0:
                        buf[(newx + int(newy / 8) * self.width)] &= ~(1 << (y % 8))

        for x in range(self.page * self.column):
            buf[x] = ~buf[x]

        return buf

    def show_image(self, pBuf):
        for i in range(0, self.page):
            self.send_command(0xB0 + i)  # set page address
            self.send_command(0x00)  # set low column address
            self.send_command(0x10)  # set high column address

            # write data #
            for j in range(0, self.column):
                self.send_data(pBuf[j + self.width * i])
