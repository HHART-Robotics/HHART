from __future__ import annotations

import asyncio
import logging

from hhart.arbitration import ROS

logger = logging.getLogger(__name__)


class RosBridge:
    """Publish telemetry here too, converted in core/ros_messages.py (Rule 4)"""

    def __init__(self) -> None:
        self._running = None
        self._switching = asyncio.Lock()

    async def set_running(self, running: bool, commands) -> str | None:
        """None, or why it failed"""
        async with self._switching:
            if running == (self._running is not None):
                return None
            if not running:
                spinning, self._running = self._running, None
                await asyncio.to_thread(spinning.close)
                if commands.driver == ROS:
                    await commands.stop(ROS)
                return None
            try:
                self._running = await asyncio.to_thread(_start, asyncio.get_running_loop(), commands)
            except Exception as exc:
                logger.warning("ROS 2 failed to start: %s", exc)
                return " ".join(str(exc).split())
            return None


def _start(loop, commands):
    from robot1.adapters.ros import Spinning
    from robot1.adapters.ros.inputs import Inputs

    spinning = Spinning("robot1")
    Inputs(spinning.node, loop, commands)
    spinning.start()
    return spinning
