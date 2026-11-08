from __future__ import annotations

from hhart.arbitration import OPERATOR
from hhart.operator import serve
from robot1.core.contract import CONTRACT, Error


async def handle_client(ws, session, publisher) -> None:
    """Client leaving mid-drive stops robot (Rule 8)"""
    await serve(ws, CONTRACT, publisher, {
        "drive": lambda m: session.drive(m.direction, m.pct, OPERATOR),
        "stop": lambda m: session.stop(OPERATOR),
        "release": lambda m: session.release(OPERATOR),
        "switch": lambda m: session.set_capability(m.name, m.running),
    }, reject=lambda text: CONTRACT.encode(Error(text)), snapshot=session.snapshot,
        moves={"drive": True, "stop": False}, on_leave=lambda: session.stop(OPERATOR))
