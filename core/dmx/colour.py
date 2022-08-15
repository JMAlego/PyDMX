"""Module for DMX colour."""

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

    def serialize(self, *args, **kwargs) -> List[int]:
        """Alias of `serialise`."""
        return self.serialise(*args, **kwargs)

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

# Alias of `Colour`.
Color = Colour
