from __future__ import annotations

import pytest

from robot1.core import ros_messages
from robot1.core.commands import DIRECTIONS, frame_from


@pytest.mark.parametrize("direction", DIRECTIONS)
def test_a_command_survives_the_trip_through_a_twist(direction):
    for pct in (10, 55, 100):
        linear, angular = ros_messages.twist_from_frame(frame_from(direction, pct))
        assert ros_messages.command_from_twist(linear, angular) == (direction, pct)


def test_rep_103_forward_is_positive_x_and_left_is_counter_clockwise():
    assert ros_messages.twist_from_frame(frame_from("forward", 100))[0] > 0
    assert ros_messages.twist_from_frame(frame_from("left", 100))[1] > 0


def test_a_twist_inside_the_deadband_is_a_stop():
    assert ros_messages.command_from_twist(0.001, 0.0) == (None, 0)
