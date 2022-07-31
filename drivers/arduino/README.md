# PyDMX-Drivers-Arduino

_This project is not affiliated with Arduino._

## Introduction

PyDMX is a package capable of sending DMX512 data via a driver.

PyDMX-Drivers-Arduino provides drivers for Arduino-based devices and hardware for PyDMX.

The PyDMX core can be found at [PyDMX](https://pypi.org/project/pydmx/).

## Drivers

### AVRDMX

The AVRDMX driver is designed to work with the [AVR-DMX](https://github.com/JMAlego/AVR-DMX) firmware I created for the Arduino Uno. It is capable of using all the modes completed on the AVR-DMX project and is effectively a reference implementation of a driver for that project. When combined with the [DMX Shield](https://github.com/JMAlego/ArDMX) I designed for the Arduino Uno it should allow for pretty easy interfacing with a DMX network.

### Dependencies

The Arduino drivers requires the python module `pyserial`.

## License

This project is licensed under the BSD 3-Clause License. See the LICENSE file for more details.
