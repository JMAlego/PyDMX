"""Module for DMX universe."""

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

from typing import Iterator, List, Set

from dmx.constants import DMX_EMPTY_BYTE, DMX_MAX_ADDRESS, DMX_MIN_ADDRESS
from dmx.light import DMXLight


def _circular_range(start: int, stop: int, modulo: int) -> Iterator[int]:
    """A circular range from start to stop mod some value."""
    counter = start
    while counter != stop and counter < modulo:
        yield counter
        counter = (counter + 1) % modulo


class DMXUniverse:
    """Represents a DMX universe."""

    def __init__(self, universe_id: int = 1):
        """Initialise the DMX universe."""
        self._lights = set()  # type: Set[DMXLight]
        self._id = universe_id

    def add_light(self, light: DMXLight):
        """Add a light to the universe."""
        self._lights.add(light)

    def remove_light(self, light: DMXLight):
        """Remove a light from the universe."""
        self._lights.remove(light)

    def has_light(self, light: DMXLight) -> bool:
        """Check if the universe has a light."""
        return light in self._lights

    def get_lights(self) -> Set[DMXLight]:
        """Get all lights in this universe."""
        return self._lights

    def serialise(self, partial: bool = False) -> List[int]:
        """Serialise all the content of the DMX universe.

        Creates a frame which will update all lights to their current state.

        If `partial` is `True` then only up to the highest light address in the
        `Universe` will be serialised.
        """
        # assume by default that we want to send a whole frame even if we don't
        # have lights configured in some sections of it
        frame_size = DMX_MAX_ADDRESS

        # if we only send what we need to (e.g. partially send the frame) we
        # have to work out how big the frame should be ahead of time
        if partial:
            if self._lights:
                # addresses are 1-indexed so the lowest address is 1 and the
                # highest is 512, as such we don't need to add one to size here
                # for it to get the frame size right
                frame_size = max(light.highest_address for light in self._lights)
            else:
                frame_size = 0

        frame = [DMX_EMPTY_BYTE] * frame_size

        for light in self._lights:
            serialised_light = light.serialise()

            # translate to zero-indexed ranges for modular range
            zero_indexed_range_start = light.start_address - DMX_MIN_ADDRESS
            zero_indexed_range_end = light.end_address

            for index, address in enumerate(
                    _circular_range(zero_indexed_range_start, zero_indexed_range_end,
                                    DMX_MAX_ADDRESS)):
                # back to real DMX address which is one-indexed
                address += DMX_MIN_ADDRESS

                if partial and len(frame) < address:
                    frame.extend([DMX_EMPTY_BYTE] * (address - len(frame)))

                # the index here is a counter for the light's internet
                frame[address - DMX_MIN_ADDRESS] |= serialised_light[index]

        return frame

    def serialize(self, *args, **kwargs) -> List[int]:
        """Alias of `serialise`."""
        return self.serialise(*args, **kwargs)
