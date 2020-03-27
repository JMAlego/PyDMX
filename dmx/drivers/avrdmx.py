#!/usr/bin/env python3
"""Driver for AVR DMX 1 Arduino DMX interface."""
from math import ceil
from os import path
from platform import system
from time import sleep
from typing import List, cast
from warnings import warn

from serial import Serial

from dmx.drivers import DMXDriver


class ProtocolException(Exception):
    """Generic exception thrown by errors communicating with the device."""


class EncodingException(Exception):
    """Error in encoding."""


class AVRDMX(DMXDriver):
    """A DMX driver design for an Arduino based interface."""

    DEFAULT_DEVICE = "COM3" if system() == "Windows" else "/dev/ttyACM0"

    class BaudratePreset:
        """Enumeration of baudrate presets."""

        START_UP = LOW_SPEED = 9600
        NORMAL_SPEED = 115200
        SAFE_HIGH_SPEED = 230400
        HIGH_SPEED = 460800
        DEFAULT = SAFE_HIGH_SPEED if system() == "Windows" else HIGH_SPEED

    class _ProtocolKey:
        """Enumeration of protocol types."""

        PROMPT = b'\x12'
        PROMPT_2 = b'\x78'
        RESPONSE = b'\x33'
        READY_FOR_PACKET = b'\x44'
        SENDING = b'\x55'
        ERROR = b'\x66'
        SENT = b'\x99'
        REPEAT_VALUE = 7

    class _PacketType:
        """Enumeration of different packet types."""

        RAW_PACKET = b'\x00'
        RLE_PACKET = b'\x01'
        SRE_PACKET = b'\x02'
        BP1_PACKET = b'\x03'
        BP2_PACKET = b'\x04'
        BP4_PACKET = b'\x05'
        SUM_PACKET = b'\x06'
        CONTROL_PACKET = b'\xff'

    class _ControlCode:
        """Enumeration of control code bytes."""

        NONE = b'\x00'
        SET_PBM_OFF = b'\x10'
        SET_PBM_ON = b'\x11'
        RESET_BR = b'\x20'
        SET_BR = b'\x21'
        SET_BR_SLOW = b'\x22'

    class Encoding:
        """Enumeration of different encoding methods."""

        RAW = RAW_DMX = "raw"
        RLE = RUN_LENGTH = "rle"
        BP1 = ONE_BIT = "1bp"
        BP2 = TWO_BIT = "2bp"
        BP4 = FOUR_BIT = "4bp"
        SUM = SUBSET_UPDATE = "sum"
        SRE = SELF_REFERENTIAL = "sre"
        TCZ = TRUNCATE_ZEROS = "tcz"

        _ENCODINGS = (RAW, RLE, BP1, BP2, BP4, SUM, SRE, TCZ)

    def __init__(self,
                 device=DEFAULT_DEVICE,
                 baudrate=BaudratePreset.DEFAULT,
                 encoding=Encoding.RAW):
        """Initialise the DMX driver.

        Parameters
        ----------
        device: str
            The device to open, defaults to /dev/ttyACM0.

        baudrate: int
            The baudrate to use for communication, defaults to the maximum.

        encoding: str
            The encoding to use for data transfer, defaults to 'raw'.

        """
        self._device = device
        self._baudrate = baudrate
        if system() == "Windows" and self._baudrate > 230400:
            warn("Setting baudrate to above 230400 baud has been found to cause issues on Windows.")
        self._serial = None
        self._closed = True
        if encoding not in AVRDMX.Encoding._ENCODINGS:
            raise EncodingException("Encoding not recognised, choose one of: '{}'.".format(
                "', '".join(AVRDMX.Encoding._ENCODINGS)))
        self._encoding = encoding

    def write_control(self, data: List[int], control_code=_ControlCode.NONE):
        """Write 512 bytes or less of control data.

        Parameters
        ----------
        data: List[int]
            512 or less bytes of data, typically configuration for the control code.

        control_code: bytes
            A single byte representing the control code to be sent.

        """
        self._write_raw(data,
                        control_code=control_code,
                        packet_type=AVRDMX._PacketType.CONTROL_PACKET)

    def change_baudrate(self, new_baudrate: int):
        """Change the baudrate used for data transfer.

        Parameters
        ----------
        new_baudrate: int
            The baudrate to change to, should fit in a unsigned 32-bit integer.

        Notes
        -----
        This method takes at least 100ms as the AVRDMX pauses to give the
        computer time to reconfigure the serial connection. This cannot be
        disabled.

        """
        # Encode the baudrate as a 32bit big-endian unsigned number and pack into bytes.
        baudrate_bytes = [(new_baudrate >> 24) & 0xff, (new_baudrate >> 16) & 0xff,
                          (new_baudrate >> 8) & 0xff, new_baudrate & 0xff]

        if system() == "Windows":
            # Windows is slow so it gets it's own way to change baudrate
            set_br_control_code = AVRDMX._ControlCode.SET_BR_SLOW
        else:
            set_br_control_code = AVRDMX._ControlCode.SET_BR

        # Send control signal to change baudrate
        self.write_control(data=baudrate_bytes, control_code=set_br_control_code)

        # AVRDMX will now change baudrate and then, after 100ms, it will send
        # a response byte at the new baudrate to confirm. During this time we
        # need to change the baudrate that we have the serial connection open
        # with, then wait for that confirmation byte.

        # Update internal baudrate setting.
        self._baudrate = new_baudrate

        # Change the serial connection to the new baudrate
        self._serial.baudrate = self._baudrate

        # Wait for confirmation of change from the AVRDMX
        response = self._serial.read(1)
        if response != AVRDMX._ProtocolKey.RESPONSE:
            self._handle_error(response)

    def _write_raw(self,
                   data: List[int],
                   packet_type: bytes = _PacketType.RAW_PACKET,
                   control_code: bytes = _ControlCode.NONE):
        """Write data without any wrapping.

        Parameters
        ----------
        data: List[int]
            The up to 512 values between 0 and 255 (inclusive) to send.

        packet_type: bytes
            The packet type to place at the start of the packet header.
            Defaults to _PacketType.RAW_PACKET or 0x00.

        control_code: bytes
            The control code, placed in the 0th slot.
            Defaults to _ControlCode.NONE or 0x00.

        """
        byte_data = bytes(data)
        if isinstance(packet_type, int):
            packet_type_bytes = bytes([packet_type])
        else:
            packet_type_bytes = cast(bytes, packet_type)

        response = self._serial.read(1)

        if response != AVRDMX._ProtocolKey.READY_FOR_PACKET:
            self._handle_error(response)

        byte_data = control_code + byte_data

        length = len(byte_data)

        length = length & 0xffff
        header = packet_type_bytes + bytes([length & 0xff, (length >> 8) & 0xff])

        self._serial.write(header + byte_data)

        response = self._serial.read(1)

        if packet_type_bytes == AVRDMX._PacketType.CONTROL_PACKET:
            if response != AVRDMX._ProtocolKey.RESPONSE:
                self._handle_error(response)

        else:
            if response != AVRDMX._ProtocolKey.SENDING:
                self._handle_error(response)

            response = self._serial.read(1)

            if response != AVRDMX._ProtocolKey.SENT:
                self._handle_error(response)

    def _encoding_xbp(self, data: List[int], bit_depth: int) -> List[int]:
        """Encode data at a specified bit depth.

        Parameters
        ----------
        data: List[int]
            The data to encode.

        bit_depth: int
            The number of bits to use to encode the data.

        Returns
        -------
        encoded_data: List[Int]
            The encoded data packed back into bytes.

        """
        values_per_byte = 8 // bit_depth
        output_data = [0] * ceil((len(data)) / float(values_per_byte))
        for index, value in enumerate(data):
            out_index = index // values_per_byte
            out_value = round((value / 0xff) * (2**bit_depth - 1))
            bit_offset = index % values_per_byte
            output_data[out_index] |= (out_value & (2**bit_depth - 1)) << (bit_depth * bit_offset)
        return output_data

    def write(self, data: List[int]):
        """Write 512 bytes or less of DMX data.

        Parameters
        ----------
        data: List[int]
            a list of up to 512 values between 0 and 255 (inclusive).

        Notes
        -----
        This function will perform any encoding needed to send the data using
        the encoding specified when the driver was initialised. Most encoding
        methods will pad the data with zeros, but some methods will truncate
        the data before sending.

        If an encoding method with a reduced bit-depth is specified, this
        method will, as part of encoding the data, round to the nearest
        representable value.

        """
        if self._encoding == AVRDMX.Encoding.RAW_DMX:
            self._write_raw(data)
        elif self._encoding == AVRDMX.Encoding.ONE_BIT:
            self._write_raw(self._encoding_xbp(data, 1), packet_type=AVRDMX._PacketType.BP1_PACKET)
        elif self._encoding == AVRDMX.Encoding.TWO_BIT:
            self._write_raw(self._encoding_xbp(data, 2), packet_type=AVRDMX._PacketType.BP2_PACKET)
        elif self._encoding == AVRDMX.Encoding.FOUR_BIT:
            self._write_raw(self._encoding_xbp(data, 4), packet_type=AVRDMX._PacketType.BP4_PACKET)

    def _handle_error(self, first_byte: bytes):
        """Handle an unexpected or error byte.

        Parameters
        ----------
        first_byte: bytes
            The byte which caused or indicated the error.

        """
        # If byte indicated error code will follow.
        if first_byte == AVRDMX._ProtocolKey.ERROR:
            error_code = self._serial.read(1)
            self.close()
            # Decode error code.
            if error_code == 0x00:
                raise ProtocolException("Null error.")
            elif error_code == 0x01:
                raise ProtocolException("Incorrect handshape first prompt.")
            elif error_code == 0x02:
                raise ProtocolException("Incorrect handshake second prompt.")
            elif error_code == 0x03:
                raise ProtocolException("Read timed-out before completion of packet header.")
            elif error_code == 0x04:
                raise ProtocolException(
                    "Received too much data. This is unlikely without memory corruption.")
            elif error_code == 0x05:
                raise ProtocolException(
                    "Read timed-out, not enough data received. Packet length might have been wrong?"
                )
            else:
                raise ProtocolException("Unknown error with code: 0x{}.".format(error_code.hex()))
        # If we received a non-error byte which was unexpected at this time.
        else:
            raise ProtocolException("Unexpected response first byte 0x{}.".format(first_byte.hex()))

    def open(self):
        """Open the driver.

        Notes
        -----
        As part of opening the driver, a "change baudrate" control message will
        be sent if it is not 9600 baud. Any further control messages required
        to configure the ARVDMX for the specified encoding mode will also be
        sent as part of opening the driver. This function will block until the
        AVRDMX confirms that the configuration has been set.

        """
        # Open serial connection.
        self._serial = Serial(self._device, AVRDMX.BaudratePreset.START_UP)

        # Wait for ping...
        response = self._serial.read(1)
        if response != AVRDMX._ProtocolKey.RESPONSE:
            self._handle_error(response)

        # Start handshake.
        self._serial.write(AVRDMX._ProtocolKey.PROMPT * AVRDMX._ProtocolKey.REPEAT_VALUE)
        response = self._serial.read(1)
        if response != AVRDMX._ProtocolKey.RESPONSE:
            self._handle_error(response)
        self._serial.write(AVRDMX._ProtocolKey.PROMPT_2 * AVRDMX._ProtocolKey.REPEAT_VALUE)

        # Handshake done, moving on to settings...

        # Change baudrate to the max supported, from the default of 9600 which
        # is always set at connect.
        if self._baudrate != AVRDMX.BaudratePreset.START_UP:
            self.change_baudrate(self._baudrate)

        if self._encoding == AVRDMX.Encoding.TRUNCATE_ZEROS:
            # Truncate zeros mode requires PBM to be off, otherwise we'll end
            # up with aliasing. This is only an issue as truncate zeros mode
            # is a software mode and doesn't have hardware support.
            self.write_control(data=[], control_code=AVRDMX._ControlCode.SET_PBM_OFF)
        else:
            # We always turn PBM mode on for encodings that it doesn't affect as it
            # will increase throughput slightly.
            self.write_control(data=[], control_code=AVRDMX._ControlCode.SET_PBM_ON)

        # We are now fully configured.

        self._closed = False

    def close(self):
        """Close the driver."""
        self._closed = True
        self._serial.close()
        self._serial = None

    @property
    def closed(self) -> bool:
        """Is the driver closed."""
        return self._closed

    @staticmethod
    def get_driver_name() -> str:
        """Get the driver name."""
        return "AVRDMX"


DRIVER_CLASS = AVRDMX

__ALL__ = ["DRIVER_CLASS"]
