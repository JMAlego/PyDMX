"""Module for DMX light definitions."""

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
from typing import List

from dmx.colour import BLACK, Colour
from dmx.constants import DMX_MAX_ADDRESS, DMX_MIN_ADDRESS


class DMXLight(ABC):
    """Represents a DMX light."""

    def __init__(self, address: int = 1):
        """Initialise the light. The base initialiser simply stores the address."""
        self._address = int(max(0, min(address, DMX_MAX_ADDRESS)))

    @abstractmethod
    def serialise(self) -> List[int]:
        """Serialise the DMX light to a sequence of bytes."""

    def serialize(self, *args, **kwargs) -> List[int]:
        """Alias of `serialise`."""
        return self.serialise(*args, **kwargs)

    @property
    def start_address(self) -> int:
        """Start address (inclusive) of the light."""
        return self._address

    @property
    def end_address(self) -> int:
        """End address (inclusive) of the light."""
        end_address = self._address + self.slot_count - 1
        if end_address > DMX_MAX_ADDRESS or end_address < DMX_MIN_ADDRESS:
            return ((end_address - DMX_MIN_ADDRESS) % DMX_MAX_ADDRESS) + DMX_MIN_ADDRESS
        return end_address

    @property
    def highest_address(self) -> int:
        """Highest address used by this light."""
        if self.end_address < self.start_address:
            return DMX_MAX_ADDRESS
        return self.end_address

    @property
    def slot_count(self) -> int:
        """Get the number of slots used by this light."""
        return 0


class DMXLight3Slot(DMXLight):
    """Represents a DMX light with RGB."""

    def __init__(self, address: int = 1):
        """Initialise the light."""
        super().__init__(address=address)
        self._colour = BLACK

    @property
    def slot_count(self) -> int:
        """Get the number of slots used by this light."""
        return 3

    def set_colour(self, colour: Colour):
        """Set the colour for the light."""
        self._colour = colour

    def set_color(self, *args, **kwargs):
        """Alias for `set_colour`."""
        self.set_colour(*args, **kwargs)

    def serialise(self) -> List[int]:
        """Serialise the DMX light to a sequence of bytes."""
        return self._colour.serialise()


class DMXLight7Slot(DMXLight3Slot):
    """Represents an DMX light with RGB, rotation, and opacity."""

    def __init__(self, address: int = 1):
        """Initialise the light."""
        super().__init__(address=address)
        self._opacity = 255
        self._coords = (0, 0, 0)

    def set_rotation(self, pitch: int, roll: int, yaw: int):
        """Set the rotation of the light, each value between 0 and 255 (inclusive)."""
        pitch = int(max(0, min(pitch, 255)))
        roll = int(max(0, min(roll, 255)))
        yaw = int(max(0, min(yaw, 255)))
        self._coords = (pitch, roll, yaw)

    def set_opacity(self, value: int):
        """Set the opacity of the light between 0 and 255 (inclusive)."""
        self._opacity = int(max(0, min(value, 255)))

    @property
    def slot_count(self) -> int:
        """Get the number of slots used by this light."""
        return 7

    def serialise(self) -> List[int]:
        """Serialise the DMX light to a sequence of bytes."""
        return super().serialise() + list(self._coords) + [self._opacity]
