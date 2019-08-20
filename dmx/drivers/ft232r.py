#!/usr/bin/env python3
from ctypes import *
from os import path

from pylibftdi import Device, Driver

from dmx.drivers import DMXDriver

DRIVER_PATH = path.abspath(path.dirname(__file__))

Driver._lib_search["libftdi"] = tuple([
    path.join(DRIVER_PATH, "libftdi.so"),
    path.join(DRIVER_PATH, "libftdi.so.1"),
    path.join(DRIVER_PATH, "libftdi1.so")
] + list(Driver._lib_search["libftdi"]))

_LIBC = cdll.LoadLibrary("libc.so.6")


class timespec(Structure):
    """A timespec."""
    _fields_ = [("tv_sec", c_long), ("tv_nsec", c_long)]


def wait_ms(milliseconds):
    """Wait for a specified number of milliseconds."""
    dummy = timespec()
    sleeper = timespec()
    sleeper.tv_sec = int(milliseconds / 1000)
    sleeper.tv_nsec = (milliseconds % 1000) * 1000000
    _LIBC.nanosleep(byref(sleeper), byref(dummy))


def wait_us(nanoseconds):
    """Wait for a specified number of nanoseconds."""
    dummy = timespec()
    sleeper = timespec()
    sleeper.tv_sec = int(nanoseconds / 1000000)
    sleeper.tv_nsec = (nanoseconds % 1000) * 1000
    _LIBC.nanosleep(byref(sleeper), byref(dummy))


class FT232R(Device, DMXDriver):
    """A DMX driver design for the University of York Serial-to-DMX usb adapter based on the FT232R."""

    _BITS_8 = 8
    _STOP_BITS_2 = 2
    _PARITY_NONE = 0
    _BREAK_OFF = 0
    _BREAK_ON = 1

    def __init__(self, *o, **k):
        Device.__init__(self, *o, mode="b", **k)
        self.baudrate = 250000
        self.ftdi_fn.ftdi_set_line_property(
            FT232R._BITS_8, FT232R._STOP_BITS_2, FT232R._PARITY_NONE)

    def write(self, data):
        try:
            byte_data = bytes(data)
        except TypeError:
            byte_data = self.encoder.encode(data)
        # Break
        self._set_break_on()
        wait_ms(10)
        # Mark after break
        self._set_break_off()
        wait_us(8)
        # Frame body
        Device.write(self, b"\x00" + byte_data)
        # Idle
        wait_ms(15)

    def _set_break_on(self):
        self.ftdi_fn.ftdi_set_line_property2(
            FT232R._BITS_8, FT232R._STOP_BITS_2, FT232R._PARITY_NONE,
            FT232R._BREAK_ON)

    def _set_break_off(self):
        self.ftdi_fn.ftdi_set_line_property2(
            FT232R._BITS_8, FT232R._STOP_BITS_2, FT232R._PARITY_NONE,
            FT232R._BREAK_OFF)

    @staticmethod
    def get_driver_name():
        return "FT232R"


DRIVER_CLASS = FT232R

__ALL__ = ["DRIVER_CLASS"]
