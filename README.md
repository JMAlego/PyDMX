# PyDMX

## Introduction

PyDMX is a package capable of sending DMX512 data via a driver. It was created to allow demonstrations on open days of DMX-based projects created at the University of York Department of Computer Science (UoY CS).

The project consists of a core package and a series of optional driver packages for particular hardware and devices.

## DMX512 Protocol

```
 Idle |       Break       |MAB|  Slot 0  |  Slot 1  |
------\                   /---\        /-\ /--------\
      |                   |   |        | | |        |
      |                   |   |        | | |        |
      \-------------------/   \--------/ \-/        \--- - - -  -  -  -

```
_Diagram of the start of a DMX packet._

DMX512 (or commonly just DMX) is a relatively simple protocol. The DMX bus is in an Idle high state between packets. A packet starts with a break of 100 μs, followed by a Mark After Break (MAB) of 12 μs, this signifies the start of the frame and the start of the "slots".

```
 S 0 1 2 3 4 5 6 7 E E
\ /-\   /---\      /--
| | |   |   |      |
| | |   |   |      |
\-/ \---/   \------/
```
_Diagram of a slot with value 0b10011000 or 152._

Each slot consists of 1 low start bit, 8 data bits, and 2 high stop bits. Each bit of a slot is 4 μs long. This corresponds to a baudrate of 250000 or 250 kbit/s (though due to breaks this is not entirely accurate). There are 512 usable slots (channels) per frame and 513 slots overall. Slot 0 is special as it signifies the type of frame being sent. 0x00 is the normal frame type and corresponds to "standard" lighting data.

A frame can contain any number of slots (beyond the type slot) up to the limit of 513 slots (including type slot). Typically the 512 usable slots are referred to as channels.

The idle period between packets must be at least 92 μs and the MAB must be at least 12 μs. Further a packet must not be longer than 1 second. There are no other requirements on timing, even on inter-slot breaks.

A light will typically take an "address" which is the channel index (starting at 1) which it will listen on. Some lights will use this as a start address and listen on some number of channels above it also if they require more than 8 bits of data.

For example a light might be set to address eight, but listen on channels 8 9, and 10. It could then use each channel as a component of an RGB colour value.

Importantly for writing software relating to DMX, the standard does not specify how to encode different types of data in slots. Therefore, each light manufacturer, or even light, does it differently. There is nothing stopping a manufacturer allowing you to select noncontiguous addresses for each 8 bit value, or any number of more convoluted solutions.

## Core

The core of PyDMX has the following classes:

- DMXUniverse: represents a DMX universe
- DMXInterface: allows simple control of a DMX driver
- DMXLight: abstract base for lights
  - DMXLight3Slot: represents a 3 slot RGB light
  - DMXLight7Slot: represents a 7 slot RGB moving light
- DMXDriver: represents a DMX output driver
  - Drivers are subclasses of this class
- Colour: represents a 24-bit RGB colour value

### Dependencies

The core modules do not depend on any other python modules or external dependencies.

## Drivers

### FTDI

_This project is not affiliated with FTDI._

#### FT232R

The FT232R driver is designed to work with the FTDI FT232R chip which is a USB to serial chip made by FTDI (Future Technology Devices International). It is specifically designed to work with the USB to DMX adapter board made by the UoY CS lab techs. It is untested with any other hardware configuration.

#### Dependencies

The FTDI drivers requires the python module `pylibftdi` which in turn requires the `libftdi` shared library be installed.

### Arduino

_This project is not affiliated with Arduino._

#### AVRDMX

The AVRDMX driver is designed to work with the [AVR-DMX](https://github.com/JMAlego/AVR-DMX) firmware I created for the Arduino Uno. It is capable of using all the modes completed on the AVR-DMX project and is effectively a reference implementation of a driver for that project. When combined with the [DMX Shield](https://github.com/JMAlego/ArDMX) I designed for the Arduino Uno it should allow for pretty easy interfacing with a DMX network.

### Built-in Drivers

#### Debug

The debug interface is designed to output to the terminal the data that would be sent to a interface hardware/drivers. It is also capable of estimating the refresh rate of signals being sent out, though this is effected by platform due to the massively slow terminal output of Windows compared to other platforms.

#### Dummy

The dummy interface does nothing. It's there simply as a placeholder for testing or any other use which does not require an actual interface.

## Usage

Below is a basic example of sending an update to turn a light purple:

```python
from dmx import Colour, DMXInterface, DMXLight3Slot, DMXUniverse

PURPLE = Colour(255, 0, 255)

# Open an interface
with DMXInterface("FT232R") as interface:
    # Create a universe
    universe = DMXUniverse()

    # Define a light
    light = DMXLight3Slot(address=8)

    # Add the light to a universe
    universe.add_light(light)

    # Update the interface's frame to be the universe's current state
    interface.set_frame(universe.serialise())

    # Send an update to the DMX network
    interface.send_update()

    # Set light to purple
    light.set_colour(PURPLE)

    # Update the interface's frame to be the universe's current state
    interface.set_frame(universe.serialise())

    # Send an update to the DMX network
    interface.send_update()
```

To run the above example you would need to install the core package `PyDMX` and the FTDI driver package `PyDMX-Drivers-FTDI`.

A further example program is available in the `examples/simple.py` file in the repository root.

## License

This project is licensed under the BSD 3-Clause License. See the LICENSE file for more details.
