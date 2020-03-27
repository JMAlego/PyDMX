#!/usr/bin/env python3
"""Dummy DMX driver."""

from typing import List

from dmx.drivers import DMXDriver


class Dummy(DMXDriver):
    """Dummy DMX driver class."""

    def __init__(self):
        """Initialise the DMX driver."""
        self._closed = True

    def write(self, data: List[int]):
        """Write 512 bytes or less of DMX data.

        Parameters
        ----------
        data: List[int]
            a list of up to 512 values between 0 and 255 (inclusive).

        """

    def open(self):
        """Open the driver."""
        self._closed = False

    def close(self):
        """Close the driver."""
        self._closed = True

    @property
    def closed(self) -> bool:
        """Is the driver closed."""
        return self._closed

    @staticmethod
    def get_driver_name() -> str:
        """Get the driver name."""
        return "Dummy"


DRIVER_CLASS = Dummy

__ALL__ = ["DRIVER_CLASS"]
