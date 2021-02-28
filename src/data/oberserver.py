from src.data.base_data import BaseData
from src.data.poller import Histos


class Observer:
    def notify(self, data: BaseData, histos: Histos):
        raise Exception('This method need to be implemented')