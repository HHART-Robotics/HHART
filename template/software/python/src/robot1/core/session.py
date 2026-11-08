from __future__ import annotations

from hhart.arbitration import Arbiter
from hhart.ports import Clock, Publisher, TelemetrySource
from robot1.core.commands import frame_from
from robot1.core.contract import CONTRACT, CapabilityState, Error, Status
from robot1.core.ports import Capability, MotorSink

DEADMAN_PERIOD_S = 0.2  # P
DEADMAN_TIMEOUT_S = 0.5  # T, T + P must fit robot's stop bound (Rule 8)


class Session:
    """route is "embedded" or "full_ros" (status.route)"""

    def __init__(self, motors: MotorSink, publisher: Publisher, clock: Clock, *, route: str,
                 sources: list[TelemetrySource] = ()) -> None:
        self.motors = motors
        self.publisher = publisher
        self.route = route
        self.sources = list(sources)
        self.arbiter = Arbiter(motors, clock, period_s=DEADMAN_PERIOD_S, timeout_s=DEADMAN_TIMEOUT_S)
        self._capabilities: dict[str, tuple[Capability, bool, str | None]] = {}
        self._latest: dict[tuple, object] = {}

    @property
    def driver(self) -> str | None:
        return self.arbiter.driver

    def snapshot(self) -> list[dict]:
        return [CONTRACT.encode(m) for m in (
            Status(connected=True, route=self.route),
            *(CapabilityState(name, running, error) for name, (_, running, error) in self._capabilities.items()),
            *self._latest.values())]

    def register_capability(self, name: str, capability: Capability, *, running: bool = False) -> None:
        self._capabilities[name] = (capability, running, None)

    async def drive(self, direction: str, pct: int, source: str) -> None:
        """ValueError if invalid. Ignored while operator stop latched, unless from operator"""
        await self.arbiter.drive(frame_from(direction, pct), source)

    async def stop(self, source: str) -> None:
        await self.arbiter.stop(source)

    async def release(self, source: str) -> None:
        self.arbiter.release(source)

    async def run_deadman(self, sleep) -> None:
        await self.arbiter.run(sleep)

    async def set_capability(self, name: str, running: bool) -> None:
        """On failure old state stays, reported not raised (Rule 5)"""
        entry = self._capabilities.get(name)
        if entry is None:
            await self.publisher.publish(CONTRACT.encode(Error(f"{name} is not available on this robot")))
            return
        capability, was, _ = entry
        error = await capability.set_running(running, self)
        now = was if error else running
        self._capabilities[name] = (capability, now, error)
        await self.publisher.publish(CONTRACT.encode(CapabilityState(name, now, error)))

    async def publish(self, message) -> None:
        self._latest[(type(message), getattr(message, "device", None))] = message
        await self.publisher.publish(CONTRACT.encode(message))

    async def run(self, gather) -> None:
        await gather(*(self._consume(source) for source in self.sources))

    async def _consume(self, source: TelemetrySource) -> None:
        async for message in source.stream():
            await self.publish(message)
