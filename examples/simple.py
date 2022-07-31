#!/usr/bin/env python3
"""Test script to show how to use module."""

from sys import exit as sys_exit
from time import sleep

from dmx import Colour, DMXInterface, DMXLight3Slot, DMXUniverse


def main():
    """Entry point function."""
    with DMXInterface("AVRDMX") as interface:

        # Define DMX universe
        universe = DMXUniverse()

        # Define DMX lights
        lights = []
        for i in range(16):
            light = DMXLight3Slot(address=1 + (3 * i))
            lights.append(light)
            universe.add_light(light)
        light = DMXLight3Slot(address=510)
        lights.append(light)
        universe.add_light(light)

        for light in lights:
            random_colour = Colour(0x88, 0x26, 0xff)
            light.set_colour(random_colour)

        # Play lights randomly for a bit
        for _ in range(2000):
            interface.set_frame(universe.serialise())
            interface.send_update()

            sleep(0.5 - (15.0 / 1000.0))

    return 0


if __name__ == "__main__":
    sys_exit(main())
