from dataclasses import dataclass


@dataclass(frozen=True)
class MotorFrame:
    left_pct: int  # -100 to 100, positive forward
    right_pct: int
