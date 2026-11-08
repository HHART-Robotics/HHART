from __future__ import annotations

import asyncio

from robot1.core.contract import Motors
from robot1.core.telemetry import MotorFrame


class Loopback:
    name = "loopback"

    def __init__(self, report_s: float = 0.1) -> None:
        self.frame = MotorFrame(0, 0)
        self._report_s = report_s

    async def send(self, frame: MotorFrame) -> None:
        self.frame = frame

    async def stop(self) -> None:
        self.frame = MotorFrame(0, 0)

    async def stream(self):
        while True:
            yield Motors(self.frame.left_pct, self.frame.right_pct)
            await asyncio.sleep(self._report_s)
