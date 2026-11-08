from __future__ import annotations

from robot1.core import protocol
from robot1.core.contract import Motors
from robot1.core.telemetry import MotorFrame


def test_the_firmware_wire_format_round_trips_and_ignores_noise():
    assert protocol.encode_motor(MotorFrame(-40, 40)) == b"M -40 40\n"
    assert protocol.decode_line(b"A -40 40\r\n") == Motors(-40, 40)
    for noise in (b"", b"boot\n", b"A 1\n", b"A x y\n", b"\xff\xfe\n"):
        assert protocol.decode_line(noise) is None
