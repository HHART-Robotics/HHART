from __future__ import annotations

from robot1.adapters.ros.devices import RosDevices
from robot1.core.contract import CONTRACT
from robot1.core.health import SILENT_S, STALE_S, STARTUP_S, Freshness


def faults(devices, now_s, graph=None):
    return [CONTRACT.encode(f) for f in devices.faults(now_s, graph)]


def test_a_missing_device_is_silent_only_after_startup():
    f = Freshness(started_s=0.0)
    assert f.state(STARTUP_S - 0.1) == "waiting"
    assert f.state(STARTUP_S) == "silent"


def test_messages_that_keep_arriving_with_a_frozen_mark_are_stale():
    f = Freshness(started_s=0.0)
    for i in range(30):
        f.update(i * 0.1, mark=(0.0, 0.0, 9.81))
    assert f.state(2.9) == "stale"


def test_a_changing_mark_is_ok_and_silence_beats_staleness():
    f = Freshness(started_s=0.0)
    for i in range(30):
        f.update(i * 0.1, mark=i)
    assert f.state(2.95) == "ok"
    assert f.state(2.95 + max(SILENT_S, STALE_S)) == "silent"


def test_the_operator_gets_one_fault_per_change_and_a_clear_on_recovery():
    devices = RosDevices("diff_drive_controller")
    devices.watch("imu", started_s=0.0)
    imu = devices.health["imu"]
    for t in (0.0, 0.5):
        imu.update(t, mark=1)
    assert faults(devices, 0.5) == []
    for t in (1.0, 1.5, 2.0):
        imu.update(t, mark=1)
    assert faults(devices, 2.0) == [
        {"type": "fault", "device": "imu", "text": f"data unchanged for {STALE_S:g} s", "active": True}]
    assert faults(devices, 2.0) == []
    imu.update(2.5, mark=2)
    assert faults(devices, 2.5) == [{"type": "fault", "device": "imu", "text": "", "active": False}]


class Graph:
    def __init__(self):
        self.publishers = 1

    def count_publishers(self, topic):
        return self.publishers


def test_another_publisher_on_the_controller_is_reported_until_it_leaves():
    devices, graph = RosDevices("diff_drive_controller"), Graph()
    assert faults(devices, 0.0, graph) == []
    graph.publishers = 2
    assert faults(devices, 0.1, graph) == [{"type": "fault", "device": "cmd", "active": True,
                                           "text": "another node is publishing on diff_drive_controller/cmd_vel"}]
    assert faults(devices, 0.2, graph) == []
    graph.publishers = 1
    assert faults(devices, 0.3, graph) == [{"type": "fault", "device": "cmd", "text": "", "active": False}]
