# PyDMX-Drivers-FTDI

_This project is not affiliated with FTDI._

## Introduction

PyDMX is a package capable of sending DMX512 data via a driver.

PyDMX-Drivers-Arduino provides drivers for FTDI-based devices and hardware for PyDMX.

The PyDMX core can be found at [PyDMX](https://pypi.org/project/pydmx/).

## Drivers

### FT232R

The FT232R driver is designed to work with the FTDI FT232R chip which is a USB to serial chip made by FTDI (Future Technology Devices International). It is specifically designed to work with the USB to DMX adapter board made by the UoY CS lab techs. It is untested with any other hardware configuration.

### Dependencies

The FTDI drivers requires the python module `pylibftdi` which in turn requires the `libftdi` shared library be installed.

## License

This project is licensed under the BSD 3-Clause License. See the LICENSE file for more details.
