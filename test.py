#!/usr/bin/env python3

from sys import exit as sys_exit
from random import randint

from dmx.interface import DMXInterface
from dmx.universe import DMXUniverse
from dmx.light import DMXLight3Slot
from dmx.colour import Colour, RED, GREEN, BLUE, BLACK, WHITE

def main():
    with DMXInterface("FT232R") as interface:
        universe = DMXUniverse()
        light = DMXLight3Slot()
        universe.add_light(light)
        for _ in range(2000):
            light.set_colour(Colour(randint(0, 255), randint(0, 255), randint(0, 255)))
            interface.set_frame(universe.serialise())
            interface.send_update()
    return 0


if __name__ == "__main__":
    sys_exit(main())