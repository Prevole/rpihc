from enum import Enum

from bitarray import bitarray

from src.config import Config
from src.data.base_data import BaseData
from src.data.oberserver import Observer
from src.data.poller import Histos, HistoType


class FanMode(Enum):
    OFF = ('off', lambda x: 0x01 | x)
    ON = ('on', lambda x: 0xFE & x)

    def __init__(self, text, op):
        self.text = text
        self.op = op


class FanController(Observer):
    def __init__(self, threshold, samples=Config.fan_default_samples):
        self._state = FanTimeState(time=samples)
        self._mode = FanMode.OFF
        self._threshold = threshold

    def mode(self):
        return self._state.mode()

    def notify(self, data: BaseData, histos: Histos):
        self._state.update(histos.histo(HistoType.TEMPERATURE).current() > self._threshold)

    def has_changed(self):
        return self._state.has_changed()

    def force_on(self):
        self._state.reset(mode=FanMode.ON)


class FanTimeState:
    def __init__(self, time):
        self._state = bitarray(time)
        self._state.setall(False)

        self._has_changed = True

        self._previous = self._state.copy()

        self._all_on = bitarray(time)
        self._all_on.setall(True)

        self._all_off = bitarray(time)
        self._all_off.setall(False)

    def update(self, current: bool):
        self._state.pop(0)
        self._state.append(current)

        if (self._state == self._all_on or self._state == self._all_off) and self._state != self._previous:
            self._previous = self._state.copy()
            self._has_changed = True

    def has_changed(self):
        if self._has_changed:
            self._has_changed = False
            return True
        else:
            return False

    def mode(self):
        if self._has_changed:
            return FanMode.ON if self._state == self._all_on else FanMode.OFF
        else:
            return FanMode.ON if self._previous == self._all_on else FanMode.OFF

    def reset(self, mode: FanMode):
        if mode == FanMode.ON:
            self._state = self._all_on.copy()
            self._previous = self._all_off.copy()
        else:
            self._state = self._all_off.copy()
            self._previous = self._all_on.copy()

        self._has_changed = True
