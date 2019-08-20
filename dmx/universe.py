from typing import Set

from dmx.light import DMXLight

DMX_MAX_ADDRESS = 512

class DMXUniverse:
    """Represents a DMX universe."""
    
    def __init__(self, universe_id=1):
        self._lights = set() # type: Set[DMXLight]
        self._id = 1

    def add_light(self, light: DMXLight):
        self._lights.add(light)

    def remove_light(self, light: DMXLight):
        self._lights.remove(light)
    
    def has_light(self, light: DMXLight):
        return light in self._lights
    
    def serialise(self):
        frame = [0] * DMX_MAX_ADDRESS
        for light in self._lights:
            serialised_light = light.serialise()
            for address in range(light.start_address, light.end_address + 1):
                frame[address - 1] |= serialised_light[address - light.start_address]
        return frame
