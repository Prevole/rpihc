from src.poe_hat.data_collector import DataCollector
from src.poe_hat.fan_mode import FanMode


class FanControl:
    def __init__(self, threshold, data_collector: DataCollector):
        self._mode = FanMode.OFF
        self._threshold = threshold
        self._data_collector = data_collector

    def mode(self):
        return self._mode

    def update(self):
        self._mode = FanMode.OFF if self._data_collector.temperature() < self._threshold else FanMode.ON

    def force_on(self):
        self._mode = FanMode.ON
