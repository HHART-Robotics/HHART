"""
Usage:

    robot1-bridge --port /dev/ttyS0
    robot1-bridge --port loopback      no hardware, just echoes back
"""

from __future__ import annotations

import argparse
import asyncio
import logging

import websockets

from hhart.clock import SystemClock
from hhart.retry import Reconnecting
from hhart.websocket_publisher import WebSocketPublisher
from robot1.adapters.firmware_link import FirmwareLink
from robot1.adapters.loopback import Loopback
from robot1.adapters.operator_server import handle_client
from robot1.adapters.ros.node import RosBridge
from robot1.core.session import Session

logger = logging.getLogger("robot1.bridge")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="robot1-bridge")
    p.add_argument("--port", default="/dev/ttyS0", help="the microcontroller's UART, or loopback")
    p.add_argument("--baud", type=int, default=115200)
    p.add_argument("--ws-port", type=int, default=8765)
    p.add_argument("--log-level", default="INFO")
    return p


async def serve(args) -> None:
    publisher = WebSocketPublisher()
    device = Loopback() if args.port == "loopback" else FirmwareLink(args.port, args.baud)
    session = Session(device, publisher, SystemClock(), route="embedded",
                      sources=[Reconnecting(device, initial_delay=2.0, max_delay=10.0)])
    # No ROS, delete this and its import
    session.register_capability("ros", RosBridge())

    async def handler(ws):
        await handle_client(ws, session, publisher)

    async with websockets.serve(handler, "0.0.0.0", args.ws_port):
        logger.info("robot1 ready (embedded, %s): ws://0.0.0.0:%d", args.port, args.ws_port)
        await asyncio.gather(session.run(asyncio.gather), session.run_deadman(asyncio.sleep))


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    logging.basicConfig(level=args.log_level.upper(), format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    try:
        asyncio.run(serve(args))
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
