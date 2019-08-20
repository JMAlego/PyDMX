from dmx.drivers import get_drivers, DMXDriver
from typing import Dict

DMX_MAX_ADDRESS = 512

class DMXInterface:
    """Represents the interface between the DMX device and a frame generation source."""

    def __init__(self, driver_name, *args, **kwards):
        self._device = None
        self._frame_state = []
        self.clear_state()
        self._set_device_driver(driver_name, *args, **kwards)

    def _set_device_driver(self, driver_name: str, *args, **kwards):
        drivers = get_drivers() # type: Dict[str, DMXDriver]
        if driver_name in drivers:
            self._device = drivers[driver_name](*args, **kwards)
        else:
            raise Exception("Unknown driver")

    def open(self):
        self._device.open()

    def send_update(self):
        if not self._device.closed:
            self._device.write(self._frame_state)

    def set_frame(self, frame):
        if not self._device.closed:
            self._frame_state = frame[:DMX_MAX_ADDRESS] + ([0] * (DMX_MAX_ADDRESS - len(frame)))

    def clear_state(self):
        self._frame_state = [0] * DMX_MAX_ADDRESS

    def close(self):
        if not self._device.closed:
            self._device.close()

    def __del__(self):
        if hasattr(self._device, "closed") and not self._device.closed:
            self._device.close()
