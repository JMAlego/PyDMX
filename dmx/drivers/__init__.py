"""Module for DMX Drivers."""
from abc import ABC, abstractmethod
from importlib import import_module
from os import listdir, path
from typing import Dict, List, Type

__ALL__ = ["DMXDriver", "get_drivers"]

DRIVER_PATH = path.abspath(path.dirname(__file__))


class DMXDriver(ABC):
    """Represents a DMX driver."""

    @abstractmethod
    def __init__(self, *args, **kwargs):
        """Initialise the DMX driver."""

    @abstractmethod
    def open(self):
        """Open the driver."""

    @abstractmethod
    def close(self):
        """Close the driver."""

    @abstractmethod
    def write(self, data: List[int]):
        """Write 512 bytes or less of DMX data."""

    @property
    @abstractmethod
    def closed(self):
        """Is the driver closed."""

    @staticmethod
    def get_driver_name():
        """Get driver name."""
        return "ABC"


def get_drivers() -> Dict[str, Type[DMXDriver]]:
    """Get a dictionary of driver names to drivers."""
    drivers = {}
    for driver_file in listdir(DRIVER_PATH):
        driver_full_path = path.join(DRIVER_PATH, driver_file)
        # We make the assumption that all drivers are .py and not in __xxx__ files.
        if path.isfile(driver_full_path) and driver_file.endswith(".py") \
           and not driver_file.startswith("__"):
            driver_name = path.splitext(driver_file)[0]
            try:
                driver_module = import_module("." + str(driver_name), "dmx.drivers")
            except ImportError:
                continue
            if hasattr(driver_module, "DRIVER_CLASS"):
                driver_class = getattr(driver_module, "DRIVER_CLASS")
                drivers[driver_class.get_driver_name()] = driver_class
    return drivers
