from src.data.data_manager import DataManager
from src.device.lcd_display import LCDDisplay
from src.device.poe_device import PoEDevice
from src.fan.fan_controller import FanController


def _init_poe_device(fan_controller: FanController):
    return PoEDevice(fan_controller=fan_controller)


def _init_lcd_display():
    return LCDDisplay()


class DeviceManager:
    def __init__(self, fan_controller: FanController):
        self._data_manager = DataManager()
        self._fan_controller = fan_controller
        self._poe_device = _init_poe_device(fan_controller=fan_controller)
        self._lcd_display = _init_lcd_display()

        self._data_manager.register(self._fan_controller)
        self._data_manager.register(self._poe_device)
        self._data_manager.register(self._lcd_display)

    def splash(self):
        self._lcd_display.splash()

    def update(self):
        self._data_manager.update()

    def clear(self):
        self._poe_device.clear()
        self._lcd_display.clear()

    def stop(self):
        self._fan_controller.force_on()
        self._poe_device.clear()
        self._lcd_display.clear()
