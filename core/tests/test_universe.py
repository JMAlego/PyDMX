"""PyDMX Universe Unit Tests."""

# BSD 3-Clause License
#
# Copyright (c) 2022, Jacob Allen
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

import unittest
from typing import List

from dmx.light import DMXLight
from dmx.universe import DMXUniverse


class _Light(DMXLight):
    """Mock light used for testing."""

    def __init__(self, address: int = 1) -> None:
        """Initialise."""
        super().__init__(address)
        self.slot_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    def serialise(self) -> List[int]:
        """Serialise the DMX light to a sequence of bytes."""
        return self.slot_values

    @property
    def slot_count(self) -> int:
        """Get the number of slots used by this light."""
        return 10


class TestDMXUniverse(unittest.TestCase):
    """Test DMX Universe class."""

    def test_empty_serialise(self) -> None:
        """Test empty universe serialisation."""
        universe = DMXUniverse()

        self.assertEqual(universe.serialise(), [0] * 512)

    def test_empty_serialise_with_partial(self) -> None:
        """Test partial empty universe serialisation.."""
        universe = DMXUniverse()

        self.assertEqual(universe.serialise(partial=True), [])

    def test_simple_light(self) -> None:
        """Test simple universe serialisation."""
        universe = DMXUniverse()
        light = _Light(address=1)
        universe.add_light(light)

        self.assertEqual(universe.serialise(), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] + ([0] * 502))

    def test_simple_light_with_partial(self) -> None:
        """Test partial simple universe serialisation.."""
        universe = DMXUniverse()
        light = _Light(address=1)
        universe.add_light(light)

        self.assertEqual(universe.serialise(partial=True), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    def test_light_high_address_looping(self) -> None:
        """Test simple universe serialisation."""
        universe = DMXUniverse()
        light = _Light(address=511)
        universe.add_light(light)

        self.assertEqual(universe.serialise(), [3, 4, 5, 6, 7, 8, 9, 10] + ([0] * 502) + [1, 2])

    def test_light_high_address_looping_with_partial(self) -> None:
        """Test partial simple universe serialisation."""
        universe = DMXUniverse()
        light = _Light(address=511)
        universe.add_light(light)

        self.assertEqual(universe.serialise(partial=True),
                         [3, 4, 5, 6, 7, 8, 9, 10] + ([0] * 502) + [1, 2])
