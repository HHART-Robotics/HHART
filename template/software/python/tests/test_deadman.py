from __future__ import annotations

import pytest

from hhart.arbitration import deadman
from robot1.core.session import DEADMAN_PERIOD_S as P, DEADMAN_TIMEOUT_S as T


def first_stop_after_silence(publish_every_s: float, phase_s: float, silent_at_s: float = 3.0) -> float:
    """Seconds from last message to first stop, ticking every P from phase_s"""
    last = (silent_at_s // publish_every_s) * publish_every_s
    driving, tick = False, phase_s
    while True:
        received = min(last, (tick // publish_every_s) * publish_every_s)
        action = deadman(tick, received, commanding=True, driving=driving, timeout_s=T)
        if action == "stop":
            return tick - last
        driving = driving or action == "drive"
        tick += P


@pytest.mark.parametrize("publish_every_s", [0.05, 0.1, 0.2, 0.45])
def test_a_silent_source_stops_within_t_to_t_plus_p_at_every_phase(publish_every_s):
    for ms in range(int(P * 1000)):
        delay = first_stop_after_silence(publish_every_s, ms / 1000)
        assert T - 1e-9 <= delay < T + P + 1e-9, (publish_every_s, ms, delay)


def test_the_bound_premise_holds():
    assert 0 < P < T
