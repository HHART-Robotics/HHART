"""
Wire format:

    host to firmware   M <left_pct> <right_pct>\\n
    firmware to host   A <left_pct> <right_pct>\\n   what the motors run, every report period
"""

from __future__ import annotations

from robot1.core.contract import Motors
from robot1.core.telemetry import MotorFrame


def encode_motor(frame: MotorFrame) -> bytes:
    return f"M {frame.left_pct} {frame.right_pct}\n".encode("ascii")


def decode_line(line: bytes) -> Motors | None:
    """None for anything but a report"""
    parts = line.decode("ascii", "replace").split()
    if len(parts) != 3 or parts[0] != "A":
        return None
    try:
        return Motors(int(parts[1]), int(parts[2]))
    except ValueError:
        return None
