"""Debug DMX driver."""

from time import time_ns
from typing import List, Optional

from dmx.drivers import DMXDriver
from dmx.light import DMXLight
from dmx.universe import DMXUniverse


class Debug(DMXDriver):
    """Debug DMX driver class."""

    def __init__(self,
                 dmx_universe: Optional[DMXUniverse] = None,
                 dmx_lights: Optional[List[DMXLight]] = None):
        """Initialise the DMX driver."""
        if dmx_universe is None and dmx_lights is None:
            raise Exception("Please pass in either dmx_universe or dmx_lights to the interface.")
        if dmx_universe is not None:
            self._lights = dmx_universe.get_lights()
        if dmx_lights is not None:
            self._lights = set(dmx_lights)
        self._closed = True
        self._last_write = 0
        self._last_frequency = 0.0
        print("Driver initialised")

    def write(self, data: List[int]):
        """Write 512 bytes or less of DMX data.

        Parameters
        ----------
        data: List[int]
            a list of up to 512 values between 0 and 255 (inclusive).

        """
        if self.closed:
            print("Write to closed interface.")
            return

        time_current = time_ns()

        print("-" * 40)
        print("Data write start")
        print("-" * 40)
        for light in sorted(self._lights, key=lambda x: x.start_address):
            print("{:03}-{:03} | {}".format(light.start_address, light.end_address,
                                            " ".join("{:02x}".format(x)
                                                     for x in light.serialise())))
        print("-" * 40)
        print("Data write end")

        time_last = self._last_write
        time_difference = time_current - time_last
        frequency = 1000000000 / time_difference

        if self._last_frequency != 0.0:
            frequency = (self._last_frequency + frequency) / 2.0

        if self._last_write == 0:
            print("No estimate on first message.")
        else:
            print("Write frequency estimate is {:.3} hrz".format(frequency))

        print("-" * 40)

        if self._last_write != 0:
            self._last_frequency = frequency
        self._last_write = time_current

    def open(self):
        """Open the driver."""
        print("Driver opened")
        self._closed = False

    def close(self):
        """Close the driver."""
        print("Driver closed")
        self._closed = True

    @property
    def closed(self) -> bool:
        """Is the driver closed."""
        print("Driver status checked, status was {}".format("closed" if self._closed else "open"))
        return self._closed

    @staticmethod
    def get_driver_name() -> str:
        """Get the driver name."""
        print("Driver name checked")
        return "Debug"


DRIVER_CLASS = Debug

__ALL__ = ["DRIVER_CLASS"]
