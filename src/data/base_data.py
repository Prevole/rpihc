import socket


class BaseData:
    def __init__(self):
        self._hostname = socket.gethostname()
        self._ip = socket.gethostbyname(self._hostname)

    def ip(self):
        return self._ip

    def hostname(self):
        return self._hostname

