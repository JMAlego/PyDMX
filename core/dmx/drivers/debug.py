"""Debug DMX driver."""

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
