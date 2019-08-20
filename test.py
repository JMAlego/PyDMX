#!/usr/bin/env python3
"""Test script to show how to use module."""

from random import randint
from sys import exit as sys_exit
from time import sleep

from dmx.colour import Colour
from dmx.interface import DMXInterface
from dmx.light import DMXLight3Slot
from dmx.universe import DMXUniverse


def main():
    """Entry point function."""
    with DMXInterface("FT232R") as interface:
        # Define DMX universe
        universe = DMXUniverse()

        # Define DMX lights
        lights = []
        for i in range(16):
            light = DMXLight3Slot(address=1 + (3 * i))
            lights.append(light)
            universe.add_light(light)

        # Play lights randomly for a bit
        for _ in range(2000):
            for light in lights:
                random_colour = Colour(randint(0, 255), randint(0, 255), randint(0, 255))
                light.set_colour(random_colour)
            interface.set_frame(universe.serialise())
            interface.send_update()
            sleep(0.2)

    return 0


if __name__ == "__main__":
    sys_exit(main())
