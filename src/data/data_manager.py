from src.data.base_data import BaseData
from src.data.oberserver import Observer
from src.data.poller import HistoPoller


class DataManager:
    def __init__(self):
        self._observers = []
        self._data = BaseData()
        self._stack_poller = HistoPoller()

    def register(self, observer: Observer):
        self._observers.append(observer)

    def update(self):
        self._stack_poller.update()

        for observer in self._observers:
            observer.notify(self._data, self._stack_poller.histos())
