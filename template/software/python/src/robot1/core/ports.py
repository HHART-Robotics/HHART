from __future__ import annotations

from typing import Protocol

from hhart.arbitration import OPERATOR, ROS, TEST  # noqa: F401
from robot1.core.telemetry import MotorFrame


class CommandPort(Protocol):

    async def drive(self, direction: str, pct: int, source: str) -> None: ...
    async def stop(self, source: str) -> None: ...
    async def release(self, source: str) -> None: ...
    async def set_capability(self, name: str, running: bool) -> None: ...


class Capability(Protocol):

    async def set_running(self, running: bool, commands: CommandPort) -> str | None: ...


class MotorSink(Protocol):
    async def send(self, frame: MotorFrame) -> None: ...
    async def stop(self) -> None: ...
