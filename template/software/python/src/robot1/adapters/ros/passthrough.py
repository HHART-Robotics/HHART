from __future__ import annotations

import time
from functools import partial
from typing import Callable

from hhart.contract import Contract, Passthrough


def message_type(entry: Passthrough):
    from rosidl_runtime_py.utilities import get_message  # Lazy so module loads without ROS (Rule 9)
    return get_message(entry.ros_type)


def payload(contract: Contract, entry: Passthrough, msg) -> dict:
    from rosidl_runtime_py.convert import message_to_ordereddict  # Lazy so module loads without ROS (Rule 9)
    return contract.passthrough_payload(entry.name, message_to_ordereddict(msg))


class PassthroughNode:
    """send must be thread-safe, e.g. run_coroutine_threadsafe(publisher.publish(m), loop)"""

    def __init__(self, contract: Contract, send: Callable[[dict], object],
                 clock: Callable[[], float] = time.monotonic) -> None:
        self.contract = contract
        self.send = send
        self.clock = clock
        self._last: dict[str, float] = {}

    def attach(self, node) -> None:
        for entry in self.contract.passthroughs:
            node.create_subscription(message_type(entry), entry.topic, partial(self._on, entry), 10)

    def _on(self, entry: Passthrough, msg) -> None:
        now = self.clock()
        if entry.due(self._last.get(entry.name), now):
            self._last[entry.name] = now
            self.send(payload(self.contract, entry, msg))
