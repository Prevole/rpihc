from enum import Enum


class FanMode(Enum):
    OFF = ('off', lambda x: 0x01 | x)
    ON = ('on', lambda x: 0xFE & x)

    def __init__(self, text, op):
        self.text = text
        self.op = op
