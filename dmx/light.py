from dmx.colour import BLACK

DMX_MAX_ADDRESS = 512
DMX_MIN_ADDRESS = 1


class DMXLight:
    """Represents a DMX light."""

    def __init__(self, address=1):
        self._address = int(max(0, min(address, DMX_MAX_ADDRESS)))

    def serialise(self):
        return []

    @property
    def start_address(self): 
        return self._address

    @property
    def end_address(self):
        end_address = self._address + self.slot_count - 1
        if end_address > DMX_MAX_ADDRESS or end_address < DMX_MIN_ADDRESS:
            return (end_address % DMX_MAX_ADDRESS) + DMX_MIN_ADDRESS
        return end_address

    @property
    def slot_count():
        return 0


class DMXLight3Slot(DMXLight):
    """Represents a DMX light with RGB."""

    def __init__(self, address=1):
        super().__init__(address=address)
        self._colour = BLACK

    @property
    def slot_count(self):
        return 3

    def set_colour(self, colour):
        self._colour

    def serialise(self):
        return self._colour.serialise()


class DMXLight7Slot(DMXLight3Slot):
    """Represents an DMX light with RGB, rotation, and opacity."""
    
    def __init__(self, address: int=1):
        super().__init__(address=address)
        self._opacity = 255
        self._coords = (0, 0, 0)

    def set_rotation(self, pitch: int , roll: int, yaw: int):
        pitch = int(max(0, min(pitch, 255)))
        roll = int(max(0, min(roll, 255)))
        yaw = int(max(0, min(yaw, 255)))
        self._coords = (pitch, roll, yaw)

    def set_opacity(self, value):
        self._opacity = int(max(0, min(value, 255)))

    @property
    def slot_count(self):
        return 7

    def serialise(self):
        return super().serialise() + list(self._coords) + [self._opacity]
