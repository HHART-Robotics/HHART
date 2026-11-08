from __future__ import annotations

import asyncio
import json

import pytest

from hhart.arbitration import OPERATOR
from hhart.clock import ManualClock
from robot1.adapters.loopback import Loopback
from robot1.adapters.operator_server import handle_client
from robot1.adapters.ros.inputs import forward
from robot1.core.commands import frame_from
from robot1.core.contract import CONTRACT, Fault
from robot1.core.session import Session
from robot1.core.telemetry import MotorFrame


class Publisher:
    def __init__(self):
        self.messages, self.clients = [], set()

    async def publish(self, message):
        self.messages.append(message)

    def add(self, ws):
        self.clients.add(ws)

    def discard(self, ws):
        self.clients.discard(ws)


class Capability:
    def __init__(self, error=None):
        self.error = error

    async def set_running(self, running, commands):
        return self.error


def session(motors=None):
    return Session(motors or Loopback(), Publisher(), ManualClock(), route="embedded")


def test_a_drive_is_validated_into_tank_tracks():
    assert frame_from("forward", 40) == MotorFrame(40, 40)
    assert frame_from("left", 140) == MotorFrame(-100, 100)
    with pytest.raises(ValueError, match="unknown direction"):
        asyncio.run(session().drive("up", 40, OPERATOR))


def test_a_new_operator_sees_the_status_capabilities_and_the_latest_of_each_message():
    s = session()
    s.register_capability("ros", Capability())
    asyncio.run(s.publish(Fault(device="imu", text="no data for 1 s", active=True)))
    asyncio.run(s.publish(Fault(device="imu", text="", active=False)))
    asyncio.run(s.publish(Fault(device="lidar", text="no data for 1 s", active=True)))
    assert [m["type"] for m in s.snapshot()] == ["status", "capability", "fault", "fault"]
    assert [m["active"] for m in s.snapshot()[2:]] == [False, True]


def test_a_capability_that_fails_keeps_its_state_and_says_why():
    s = session()
    s.register_capability("ros", Capability("rclpy not found"))
    asyncio.run(s.set_capability("ros", True))
    asyncio.run(s.set_capability("lidar", True))
    assert s.publisher.messages == [{"type": "capability", "name": "ros", "running": False, "error": "rclpy not found"},
                                    {"type": "error", "text": "lidar is not available on this robot"}]


def test_a_ros_zero_ends_only_a_drive_that_ros_holds():
    async def run():
        s = session()
        await forward(s, "forward", 40)
        await forward(s, None, 0)
        stopped = s.motors.frame
        await s.drive("left", 30, OPERATOR)
        await forward(s, None, 0)
        return stopped, s.motors.frame, s.driver
    assert asyncio.run(run()) == (MotorFrame(0, 0), MotorFrame(-30, 30), OPERATOR)


class Socket:
    def __init__(self, *incoming):
        self.incoming, self.sent = [json.dumps(m) for m in incoming], []

    async def send(self, text):
        self.sent.append(json.loads(text))

    def __aiter__(self):
        return self._messages()

    async def _messages(self):
        for raw in self.incoming:
            yield raw


def test_the_operator_drives_the_loopback_and_leaving_mid_drive_stops_it():
    async def run():
        s = session()
        ws = Socket({"type": "drive", "direction": "right", "pct": 50})
        await handle_client(ws, s, s.publisher)
        return ws.sent, s.motors.frame, s.driver
    sent, frame, driver = asyncio.run(run())
    assert sent[0] == CONTRACT.describe() and sent[1]["type"] == "status"
    assert frame == MotorFrame(0, 0) and driver is None


def test_an_operator_stop_latches_ros_out_until_the_operator_releases():
    async def run():
        s = session()
        await forward(s, "forward", 40)
        await handle_client(Socket({"type": "stop"}), s, s.publisher)
        await forward(s, "forward", 40)
        refused = s.motors.frame
        await handle_client(Socket({"type": "release"}), s, s.publisher)
        await forward(s, "forward", 40)
        return refused, s.motors.frame
    assert asyncio.run(run()) == (MotorFrame(0, 0), MotorFrame(40, 40))
