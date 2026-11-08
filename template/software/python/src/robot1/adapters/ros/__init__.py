from __future__ import annotations

import threading


class Spinning:
    """Callbacks run on spin thread, not event loop"""

    def __init__(self, name: str) -> None:
        import rclpy
        from rclpy.context import Context
        from rclpy.executors import ExternalShutdownException, SingleThreadedExecutor

        self.context = Context()
        rclpy.init(context=self.context)
        self.node = rclpy.create_node(name, context=self.context)
        self._executor = SingleThreadedExecutor(context=self.context)
        self._executor.add_node(self.node)
        self._shutdown = ExternalShutdownException
        self._thread = threading.Thread(target=self._spin, name=f"ros-{name}", daemon=True)

    def start(self) -> None:
        self._thread.start()

    def _spin(self) -> None:
        try:
            self._executor.spin()
        except self._shutdown:
            pass

    def close(self) -> None:
        self._executor.shutdown()
        self.node.destroy_node()
        self.context.try_shutdown()
        self._thread.join(timeout=2.0)
