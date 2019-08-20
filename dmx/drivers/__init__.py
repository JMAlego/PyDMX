from abc import ABC, abstractmethod
from functools import partial
from importlib import import_module
from os import listdir, path
from typing import Dict


__ALL__ = ["DMXDriver", "get_drivers"]

DRIVER_PATH = path.abspath(path.dirname(__file__))

add_driver_path = partial(path.join, DRIVER_PATH)


class DMXDriver(ABC):
    
    @abstractmethod
    def open(self):
        """Open the driver."""

    @abstractmethod
    def close(self):
        """Close the driver."""

    @abstractmethod
    def write(self):
        """Write 512 bytes or less of DMX data."""

    @property
    @abstractmethod
    def closed(self):
        """Is the driver closed."""

    @staticmethod
    def get_driver_name(self):
        """Get driver name."""
        return "ABD"


def get_drivers() -> Dict[str, DMXDriver]:
    driver_files = map(add_driver_path, listdir(DRIVER_PATH))
    driver_files = filter(path.isfile, driver_files)
    driver_files = filter(lambda x: x.endswith(".py"), driver_files)
    driver_files = filter(lambda x: not path.basename(x).startswith("__"), driver_files)
    driver_names = map(path.basename, driver_files)
    driver_names = map(lambda x: path.splitext(x)[0], driver_names)
    drivers = {}
    for driver_name in driver_names:
        driver_module = import_module("." + driver_name, "dmx.drivers")
        if hasattr(driver_module, "DRIVER_CLASS"):
            driver_class = getattr(driver_module, "DRIVER_CLASS")
            drivers[driver_class.get_driver_name()] = driver_class
    return drivers
