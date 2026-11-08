from __future__ import annotations

from robot1.core.contract import Fault

STARTUP_S = 5.0  # Driver start-up grace before missing device counts as silent
SILENT_S = 1.0
STALE_S = 1.0


class Freshness:
    """mark: changes while source lives (seq number, noisy reading), not republisher's stamp"""

    def __init__(self, started_s: float) -> None:
        self.started_s = started_s
        self.seen_s: float | None = None
        self.changed_s = started_s
        self.mark: object = object()

    def update(self, now_s: float, mark: object) -> None:
        self.seen_s = now_s
        if mark != self.mark:
            self.mark, self.changed_s = mark, now_s

    def state(self, now_s: float) -> str:
        """"waiting", "ok", "silent" or "stale"."""
        if self.seen_s is None:
            return "silent" if now_s - self.started_s >= STARTUP_S else "waiting"
        if now_s - self.seen_s >= SILENT_S:
            return "silent"
        if now_s - self.changed_s >= STALE_S:
            return "stale"
        return "ok"


def health_faults(devices: dict[str, Freshness], now_s: float, reported: dict[str, str]) -> list[Fault]:
    """Faults for changes since last call, plus clear on recovery"""
    faults = []
    for name, device in devices.items():
        state = device.state(now_s)
        if state == "waiting" or state == reported.get(name, "ok"):
            continue
        reported[name] = state
        if state == "silent":
            faults.append(Fault(device=name, text=f"no data for {SILENT_S:g} s", active=True))
        elif state == "stale":
            faults.append(Fault(device=name, text=f"data unchanged for {STALE_S:g} s", active=True))
        else:
            faults.append(Fault(device=name, text="", active=False))
    return faults
