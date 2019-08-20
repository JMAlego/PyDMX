"""Module for DMX colour."""

from typing import List, Union


class Colour:
    """Represents a colour in 24 bit RGB."""

    def __init__(self, red: int, green: int, blue: int):
        """Initialise the colour."""
        self._red = red
        self._green = green
        self._blue = blue

    def serialise(self) -> List[int]:
        """Serialise the colour in RGB order to a sequence of bytes."""
        return [self._red, self._green, self._blue]

    @property
    def red(self) -> int:
        """Get red component."""
        return self._red

    @red.setter
    def red(self, value: int):
        """Set red component."""
        self._red = int(max(0, min(value, 255)))

    @property
    def green(self) -> int:
        """Get green component."""
        return self._green

    @green.setter
    def green(self, value: int):
        """Set green component."""
        self._green = int(max(0, min(value, 255)))

    @property
    def blue(self) -> int:
        """Get blue component."""
        return self._red

    @blue.setter
    def blue(self, value: int):
        """Set blue component."""
        self._blue = int(max(0, min(value, 255)))

    def __add__(self, other: Union['Colour', int, float]):
        """Handle add."""
        if isinstance(other, Colour):
            self.red += other.red
            self.green += other.green
            self.blue += other.blue
        elif isinstance(other, (int, float)):
            self.red = int(self.red + other)
            self.green = int(self.green + other)
            self.blue = int(self.blue + other)

    def __sub__(self, other: Union['Colour', int, float]):
        """Handle subtract."""
        if isinstance(other, Colour):
            self.red -= other.red
            self.green -= other.green
            self.blue -= other.blue
        elif isinstance(other, (int, float)):
            self.red = int(self.red - other)
            self.green = int(self.green - other)
            self.blue = int(self.blue - other)

    def __mul__(self, other: Union['Colour', int, float]):
        """Handle multiply."""
        if isinstance(other, Colour):
            self.red *= other.red
            self.green *= other.green
            self.blue *= other.blue
        elif isinstance(other, (int, float)):
            self.red = int(self.red * other)
            self.green = int(self.green * other)
            self.blue = int(self.blue * other)

    def __truediv__(self, other: Union['Colour', int, float]):
        """Handle division."""
        if isinstance(other, Colour):
            self.red = int(self.red / other.red)
            self.green = int(self.green / other.green)
            self.blue = int(self.blue / other.blue)
        elif isinstance(other, (int, float)):
            self.red = int(self.red / other)
            self.green = int(self.green / other)
            self.blue = int(self.blue / other)

    def __floordiv__(self, other: Union['Colour', int, float]):
        """Handle floor division."""
        if isinstance(other, Colour):
            self.red //= other.red
            self.green //= other.green
            self.blue //= other.blue
        elif isinstance(other, (int, float)):
            self.red = int(self.red // other)
            self.green = int(self.green // other)
            self.blue = int(self.blue // other)


RED = Colour(255, 0, 0)
GREEN = Colour(0, 255, 0)
BLUE = Colour(0, 0, 255)
WHITE = Colour(255, 255, 255)
BLACK = Colour(0, 0, 0)
