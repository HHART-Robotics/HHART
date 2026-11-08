from __future__ import annotations

from robot1.core.telemetry import MotorFrame

# (left, right) signs, turns on spot
DIRECTIONS = {"forward": (1, 1), "backward": (-1, -1), "left": (-1, 1), "right": (1, -1)}


def frame_from(direction: str, pct: int) -> MotorFrame:
    """ValueError if invalid, pct clamped to 0-100"""
    if direction not in DIRECTIONS:
        raise ValueError(f"unknown direction {direction!r}; expected one of: {', '.join(DIRECTIONS)}")
    pct = max(0, min(100, int(pct)))
    left, right = DIRECTIONS[direction]
    return MotorFrame(left * pct, right * pct)
