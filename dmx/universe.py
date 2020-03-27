"""Module for DMX universe."""
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
