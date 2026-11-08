from __future__ import annotations

import pytest

pytest.importorskip("rosidl_runtime_py")

from robot1.adapters.ros.passthrough import PassthroughNode, message_type, payload  # noqa: E402
from robot1.core.contract import CONTRACT  # noqa: E402


class FakeNode:
    def __init__(self) -> None:
        self.subscriptions = []

    def create_subscription(self, msg_type, topic, callback, qos):
        self.subscriptions.append((msg_type, topic, callback))


@pytest.mark.parametrize("entry", CONTRACT.passthroughs, ids=lambda e: e.name)
def test_every_declared_topic_resolves_and_every_field_path_exists(entry):
    msg = message_type(entry)()
    assert set(payload(CONTRACT, entry, msg)) == {"type", *entry.fields}


def test_the_node_subscribes_every_entry_and_throttles_to_max_hz():
    sent, now = [], [0.0]
    node = FakeNode()
    PassthroughNode(CONTRACT, sent.append, clock=lambda: now[0]).attach(node)
    assert [t for _, t, _ in node.subscriptions] == [e.topic for e in CONTRACT.passthroughs]
    msg_type, _, callback = node.subscriptions[0]
    callback(msg_type())
    callback(msg_type())
    now[0] = 2.0
    callback(msg_type())
    assert len(sent) == 2 and sent[0]["type"] == CONTRACT.passthroughs[0].name
