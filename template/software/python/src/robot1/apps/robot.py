"""
Usage:

    robot1-robot --controller diff_drive_controller   (started by robot1_bringup)
"""

from __future__ import annotations

import argparse
import asyncio
import logging

import websockets

from hhart.clock import SystemClock
from hhart.websocket_publisher import WebSocketPublisher
from robot1.adapters.operator_server import handle_client
from robot1.adapters.ros.devices import RosDevices
from robot1.core.session import Session

logger = logging.getLogger("robot1.robot")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="robot1-robot")
    p.add_argument("--controller", default="diff_drive_controller")
    p.add_argument("--ws-port", type=int, default=8765)
    p.add_argument("--log-level", default="INFO")
    return p


async def serve(args) -> None:
    publisher = WebSocketPublisher()
    devices = RosDevices(args.controller)
    session = Session(devices, publisher, SystemClock(), route="full_ros")
    devices.open(asyncio.get_running_loop(), session)

    async def handler(ws):
        await handle_client(ws, session, publisher)

    try:
        async with websockets.serve(handler, "0.0.0.0", args.ws_port):
            logger.info("robot1 ready (full ROS 2, %s): ws://0.0.0.0:%d", args.controller, args.ws_port)
            await asyncio.gather(session.run(asyncio.gather), session.run_deadman(asyncio.sleep),
                                 devices.report(session))
    finally:
        devices.close()


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
