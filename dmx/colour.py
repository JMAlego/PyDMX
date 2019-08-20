class Colour:

    def __init__(self, red, green, blue):
        self._red = red
        self._green = green
        self._blue = blue

    def serialise(self):
        return [self._red, self._green, self._blue]

    @property
    def red(self):
        return self._red

    @red.setter
    def red(self, value):
        self._red = int(max(0, min(value, 255)))

    @property
    def green(self):
        return self._green

    @green.setter
    def green(self, value):
        self._green = int(max(0, min(value, 255)))

    @property
    def blue(self):
        return self._red

    @blue.setter
    def blue(self, value):
        self._blue = int(max(0, min(value, 255)))

    def __add__(self, other):
        if isinstance(other, Colour):
            self.red += other.red
            self.green += other.green
            self.blue += other.blue
        elif isinstance(other, (int, float)):
            self.red += other
            self.green += other
            self.blue += other

    def __sub__(self, other):
        if isinstance(other, Colour):
            self.red -= other.red
            self.green -= other.green
            self.blue -= other.blue
        elif isinstance(other, (int, float)):
            self.red -= other
            self.green -= other
            self.blue -= other

    def __mul__(self, other):
        if isinstance(other, Colour):
            self.red *= other.red
            self.green *= other.green
            self.blue *= other.blue
        elif isinstance(other, (int, float)):
            self.red *= other
            self.green *= other
            self.blue *= other

    def __truediv__(self, other):
        if isinstance(other, Colour):
            self.red /= other.red
            self.green /= other.green
            self.blue /= other.blue
        elif isinstance(other, (int, float)):
            self.red /= other
            self.green /= other
            self.blue /= other

    def __floordiv__(self, other):
        if isinstance(other, Colour):
            self.red //= other.red
            self.green //= other.green
            self.blue //= other.blue
        elif isinstance(other, (int, float)):
            self.red //= other
            self.green //= other
            self.blue //= other


RED = Colour(255, 0, 0)
GREEN = Colour(0, 255, 0)
BLUE = Colour(0, 0, 255)
WHITE = Colour(255, 255, 255)
BLACK = Colour(0, 0, 0)
