from enum import Enum

import psutil

from src.config import Config


class HistoType(Enum):
    CPU = 'cpu'
    MEMORY = 'memory'
    TEMPERATURE = 'temperature'


class Histo:
    def __init__(self, size, max_value):
        self._size = size
        self._elements = [-1] * self._size
        self._max_value = max_value

    def add(self, value):
        self._elements.append(value)
        self._elements.pop(0)

    def values(self):
        copy = self._elements.copy()
        copy.reverse()
        return copy

    def size(self):
        return self._size

    def max(self):
        return self._max_value

    def current(self):
        return self._elements[self._size - 1]


class Histos:
    def __init__(self):
        self._histos = {
            HistoType.CPU: Histo(Config.number_of_samples, 100.0),
            HistoType.MEMORY: Histo(Config.number_of_samples, psutil.virtual_memory().total),
            HistoType.TEMPERATURE: Histo(Config.number_of_samples, Config.cpu_temp_max_value)
        }

    def update(self, histo_type: HistoType, value):
        self.histo(histo_type).add(value)

    def histo(self, histo_type: HistoType):
        if histo_type in self._histos:
            return self._histos.get(histo_type)
        else:
            raise Exception(f'No histo registered for {histo_type}')


class HistoPoller:
    def __init__(self):
        self._histos = Histos()

    def update(self):
        mem_stats = psutil.virtual_memory()

        self._histos.update(HistoType.MEMORY, mem_stats.total - mem_stats.available)
        self._histos.update(HistoType.CPU, psutil.cpu_percent())
        self._histos.update(HistoType.TEMPERATURE, self._temperature())

    def histos(self):
        return self._histos

    @staticmethod
    def _temperature():
        with open('/sys/class/thermal/thermal_zone0/temp', 'rt') as f:
            temp = int(f.read()) / 1000.0

        return int(temp * 10) / 10.0
