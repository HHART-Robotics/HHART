"""REP 103: x forward, z up, CCW positive."""

from __future__ import annotations

from robot1.core.telemetry import MotorFrame

MAX_MPS = 0.3   # Track speed at 100 %, measure on robot
TRACK_M = 0.2   # Centre to centre of tracks or wheels
DEADBAND = 0.02  # Fraction of MAX_MPS, below is stop


def twist_from_frame(frame: MotorFrame, max_mps: float = MAX_MPS, track_m: float = TRACK_M) -> tuple[float, float]:
    """(linear.x m/s, angular.z rad/s) for diff drive controller"""
    left, right = frame.left_pct / 100 * max_mps, frame.right_pct / 100 * max_mps
    return (left + right) / 2, (right - left) / track_m


def command_from_twist(linear_mps: float, angular_rps: float, max_mps: float = MAX_MPS,
                       track_m: float = TRACK_M) -> tuple[str | None, int]:
    """(direction, pct) on dominant axis, (None, 0) for stop. Command port takes no blends"""
    turn_mps = abs(angular_rps) * track_m / 2
    if max(abs(linear_mps), turn_mps) < DEADBAND * max_mps:
        return None, 0
    if abs(linear_mps) >= turn_mps:
        direction, speed = ("forward" if linear_mps > 0 else "backward"), abs(linear_mps)
    else:
        direction, speed = ("left" if angular_rps > 0 else "right"), turn_mps
    return direction, min(100, round(speed / max_mps * 100))
