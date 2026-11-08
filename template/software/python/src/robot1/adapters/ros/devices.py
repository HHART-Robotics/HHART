from __future__ import annotations

import asyncio
import time

from robot1.core import ros_messages
from robot1.core.contract import CONTRACT, Fault
from robot1.core.health import Freshness, health_faults
from robot1.core.telemetry import MotorFrame


class RosDevices:

    def __init__(self, controller: str) -> None:
        self.controller = controller
        self.cmd_topic = f"{controller}/cmd_vel"
        self.health: dict[str, Freshness] = {}
        self._reported: dict[str, str] = {}
        self._spinning = None
        self._cmd = None

    def open(self, loop: asyncio.AbstractEventLoop, session) -> None:
        from geometry_msgs.msg import TwistStamped
        from nav_msgs.msg import Odometry

        from robot1.adapters.ros import Spinning
        from robot1.adapters.ros.inputs import Inputs
        from robot1.adapters.ros.passthrough import PassthroughNode

        self._loop, self._twist = loop, TwistStamped
        self._spinning = Spinning("robot1_devices")
        node = self._spinning.node
        self._cmd = node.create_publisher(TwistStamped, self.cmd_topic, 10)
        self.watch("odometry", time.monotonic())
        node.create_subscription(Odometry, f"{self.controller}/odom", self._on_odom, 10)
        Inputs(node, loop, session)
        PassthroughNode(CONTRACT, lambda m: asyncio.run_coroutine_threadsafe(
            session.publisher.publish(m), loop)).attach(node)
        self._spinning.start()

    def close(self) -> None:
        if self._spinning is not None:
            self._spinning.close()

    def watch(self, device: str, started_s: float) -> None:
        """Then call self.health[device].update(now, mark) from device's callback"""
        self.health[device] = Freshness(started_s)

    def _on_odom(self, msg) -> None:
        # Stamp as mark, odom at rest repeats pose so only silence is a fault
        mark = (msg.header.stamp.sec, msg.header.stamp.nanosec)
        self._loop.call_soon_threadsafe(self.health["odometry"].update, time.monotonic(), mark)

    def faults(self, now_s: float, graph=None) -> list[Fault]:
        found = health_faults(self.health, now_s, self._reported)
        if graph is not None:
            shared = graph.count_publishers(self.cmd_topic) > 1
            if shared != (self._reported.get("cmd") == "shared"):
                self._reported["cmd"] = "shared" if shared else "ok"
                text = f"another node is publishing on {self.cmd_topic}" if shared else ""
                found.append(Fault(device="cmd", text=text, active=shared))
        return found

    async def report(self, session, period_s: float = 0.25) -> None:
        while True:
            await asyncio.sleep(period_s)
            graph = self._spinning.node if self._spinning is not None else None
            for fault in self.faults(time.monotonic(), graph):
                await session.publish(fault)

    async def send(self, frame: MotorFrame) -> None:
        self._publish(*ros_messages.twist_from_frame(frame))

    async def stop(self) -> None:
        self._publish(0.0, 0.0)

    def _publish(self, linear_mps: float, angular_rps: float) -> None:
        if self._cmd is None:
            raise ConnectionError("ROS devices are not open")
        msg = self._twist()
        msg.header.stamp = self._spinning.node.get_clock().now().to_msg()
        msg.header.frame_id = "base_link"
        msg.twist.linear.x, msg.twist.angular.z = linear_mps, angular_rps
        self._cmd.publish(msg)
