from bitarray import bitarray

from src.poe_hat.data_collector import DataCollector
from src.poe_hat.fan_mode import FanMode


class FanControl:
    def __init__(self, threshold, data_collector: DataCollector, samples=10):
        self._state = FanTimeState(time=samples)
        self._mode = FanMode.OFF
        self._threshold = threshold
        self._data_collector = data_collector

    def mode(self):
        return self._state.mode()

    def update(self):
        self._state.update(self._data_collector.temperature() > self._threshold)

        # self._mode = FanMode.OFF if self._data_collector.temperature() < self._threshold else FanMode.ON

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
