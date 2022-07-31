"""Module for DMX Drivers."""

# BSD 3-Clause License
#
# Copyright (c) 2019-2022, Jacob Allen
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from abc import ABC, abstractmethod
from importlib import import_module
from os import listdir, path, walk
from typing import Dict, List, Type

DMX_DRIVERS_PRESENT = True
try:
    # Do we have any extended drivers installed?
    import dmx_drivers
except ImportError:
    dmx_drivers = None
    DMX_DRIVERS_PRESENT = False

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

    # There are two possible sources of "containers" for drivers, all drivers
    # that come with PyDMX, and drivers from PyDMX-Drivers-??? packages.
    driver_containers = [DRIVER_PATH]
    if DMX_DRIVERS_PRESENT and hasattr(dmx_drivers, "__path__"):
        for driver_path in dmx_drivers.__path__:
            driver_containers += [path.join(driver_path, x) for x in listdir(driver_path)]

    # We go through each container, looking for drivers...
    for driver_container in driver_containers:
        # Drivers must be in their own files, so we look based on files...
        for driver_file in listdir(driver_container):
            container_name = path.basename(driver_container)
            driver_full_path = path.join(driver_container, driver_file)

            # We make the assumption that all drivers are .py and not in __xxx__ files.
            if (path.isfile(driver_full_path) and driver_file.endswith(".py")
                    and not driver_file.startswith("__")):
                driver_name, *_ = path.splitext(driver_file)

                # We try to import the driver here, just in case it's not actually a driver.
                try:
                    from_package = "dmx.drivers"
                    if container_name != "drivers":
                        from_package = "dmx_drivers." + container_name

                    driver_module = import_module("." + str(driver_name), from_package)
                except ImportError:
                    continue  # there's an error in the driver, continue.

                # If it's actually a driver it will specify a "DRIVER_CLASS" to load.
                if hasattr(driver_module, "DRIVER_CLASS"):
                    driver_class = getattr(driver_module, "DRIVER_CLASS")
                    drivers[driver_class.get_driver_name()] = driver_class

    return drivers
