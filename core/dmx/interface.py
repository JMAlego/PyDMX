"""Module for DMX interface."""

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

from typing import List, Optional

from dmx.constants import DMX_MAX_ADDRESS
from dmx.drivers import DMXDriver, get_drivers


class DMXInterface:
    """Represents the interface between the DMX device and a frame generation source."""

    def __init__(self, driver_name: str, *args, **kwards):
        """Initialise the DMX interface."""
        self._device = None  #  type: Optional[DMXDriver]
        self._frame_state = []  # type: List[int]
        self.clear_state()
        self._set_device_driver(driver_name, *args, **kwards)

    def _set_device_driver(self, driver_name: str, *args, **kwards):
        """Set driver to specified driver."""
        drivers = get_drivers()
        if driver_name in drivers:
            driver = drivers[driver_name]
            self._device = driver(*args, **kwards)
        else:
            raise Exception("Unknown driver")

    def __enter__(self):
        """Open interface, for use with the 'with' statement."""
        self.open()
        return self

    def __exit__(self, *k):
        """Close interface, for use with the 'with' statement."""
        self.close()

    def open(self):
        """Open interface."""
        self._device.open()

    def send_update(self):
        """Send an update on the interface."""
        if self._device is not None and not self._device.closed:
            self._device.write(self._frame_state)

    def set_frame(self, frame: List[int]):
        """Set the current state of the next DMX frame to be sent on the interface."""
        if self._device is not None and not self._device.closed:
            self._frame_state = frame[:DMX_MAX_ADDRESS] + ([0] * (DMX_MAX_ADDRESS - len(frame)))

    def clear_state(self):
        """Clear the state of the next DMX frame."""
        self._frame_state = [0] * DMX_MAX_ADDRESS

    def close(self):
        """Close the interface."""
        if self._device is not None and not self._device.closed:
            self._device.close()

    def __del__(self):
        """Try and close the driver if this object is disposed."""
        if self._device is not None and hasattr(self._device, "closed") and not self._device.closed:
            self._device.close()
