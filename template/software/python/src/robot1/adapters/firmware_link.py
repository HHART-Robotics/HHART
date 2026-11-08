from __future__ import annotations

from robot1.core import protocol
from robot1.core.telemetry import MotorFrame


class FirmwareLink:
    name = "firmware"

    def __init__(self, port: str, baud: int = 115200) -> None:
        self.port = port
        self.baud = baud
        self._writer = None

    async def stream(self):
        """Wrap in Reconnecting so dropped link reopens"""
        import serial_asyncio  # Embedded extra, lazy so root loads without it

        reader, self._writer = await serial_asyncio.open_serial_connection(url=self.port, baudrate=self.baud)
        try:
            while True:
                message = protocol.decode_line(await reader.readline())
                if message is not None:
                    yield message
        finally:
            self._writer.close()
            self._writer = None

    async def send(self, frame: MotorFrame) -> None:
        if self._writer is None:
            raise ConnectionError(f"{self.port} is not open")
        self._writer.write(protocol.encode_motor(frame))
        await self._writer.drain()

    async def stop(self) -> None:
        await self.send(MotorFrame(0, 0))
