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

from typing import List, Set

from dmx.constants import DMX_MAX_ADDRESS
from dmx.light import DMXLight


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

    def serialise(self) -> List[int]:
        """Serialise all the content of the DMX universe.

        Creates a frame which will update all lights to their current state.
        """
        frame = [0] * DMX_MAX_ADDRESS
        for light in self._lights:
            serialised_light = light.serialise()
            for address in range(light.start_address, light.end_address + 1):
                frame[address - 1] |= serialised_light[address - light.start_address]
        return frame
