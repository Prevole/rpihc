import socket


class DataCollector:
    def __init__(self):
        self._ip = None

    def ip(self):
        if self._ip is None:
            hostname = socket.gethostname()
            self._ip = socket.gethostbyname(hostname)

        return self._ip

    @staticmethod
    def temperature():
        with open('/sys/class/thermal/thermal_zone0/temp', 'rt') as f:
            temp = int(f.read()) / 1000.0

        return int(temp * 10) / 10.0
