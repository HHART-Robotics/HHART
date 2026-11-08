from __future__ import annotations

import asyncio
import logging

from hhart.arbitration import ROS
from robot1.core import ros_messages

logger = logging.getLogger(__name__)


async def forward(commands, direction: str | None, pct: int) -> None:
    """Zero only ends ROS's own drive, so idle ROS client can't stop operator"""
    try:
        if direction is not None:
            await commands.drive(direction, pct, ROS)
        elif commands.driver == ROS:
            await commands.stop(ROS)
    except Exception as exc:
        logger.warning("ROS command failed: %s", exc)


class Inputs:
    def __init__(self, node, loop: asyncio.AbstractEventLoop, commands) -> None:
        from geometry_msgs.msg import Twist

        self._loop = loop
        self.commands = commands
        node.create_subscription(Twist, "cmd_vel", self._on_twist, 10)

    def _on_twist(self, msg) -> None:
        direction, pct = ros_messages.command_from_twist(msg.linear.x, msg.angular.z)
        # Schedule, don't await, waiting here deadlocks executor
        asyncio.run_coroutine_threadsafe(forward(self.commands, direction, pct), self._loop)
