from __future__ import annotations

from dataclasses import dataclass

from hhart.contract import IN, Contract

# Bump on rename or removal, not additions
CONTRACT = Contract(version="0.1.0")


@CONTRACT.message("status")
@dataclass(frozen=True)
class Status:
    connected: bool
    route: str  # "embedded" or "full_ros"


@CONTRACT.message("fault")
@dataclass(frozen=True)
class Fault:
    device: str
    text: str
    active: bool  # False clears device's fault


@CONTRACT.message("error")
@dataclass(frozen=True)
class Error:
    text: str


@CONTRACT.message("motors")
@dataclass(frozen=True)
class Motors:
    left_pct: int  # As run by device, -100 to 100
    right_pct: int


@CONTRACT.message("capability")
@dataclass(frozen=True)
class CapabilityState:
    name: str
    running: bool
    error: str | None


@CONTRACT.message("drive", direction=IN)
@dataclass(frozen=True)
class Drive:
    direction: str
    pct: int


@CONTRACT.message("stop", direction=IN)
@dataclass(frozen=True)
class Stop:
    pass


@CONTRACT.message("release", direction=IN)
@dataclass(frozen=True)
class Release:
    pass


@CONTRACT.message("switch", direction=IN)
@dataclass(frozen=True)
class Switch:
    name: str
    running: bool


# BatteryState.percentage is 0-1, not %
CONTRACT.passthrough("battery", topic="/battery_state", ros_type="sensor_msgs/msg/BatteryState",
                     fields={"voltage_v": "voltage", "charge": "percentage"},
                     units={"voltage_v": "V", "charge": "0 to 1"}, max_hz=1.0)
