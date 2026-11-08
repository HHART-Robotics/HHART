# Agent instructions

This robot is built on HHART. The rules are in the top-level README and
enforced by tests.

## Before finishing

From `software/`:

```text
cd python && pytest
hhart check ..
cd .. && pnpm test && pnpm typecheck && pnpm build
cd firmware/robot1 && uvx --from platformio pio test -e native
```

After changing `python/src/robot1/core/contract.py`, run `hhart contract`
first. For UI work see [FRONTEND.md](FRONTEND.md).

Never weaken, skip or delete a test to make it pass.

## Free to change

- Views and layout in `apps/web/src/` (see [FRONTEND.md](FRONTEND.md) and
  [DESIGN.md](DESIGN.md)). Shared panels and styles belong in `@hhart/ui`.
- Adapter internals, as long as the port stays the same.
- Docs.

## Ask first

- `core/session.py`: deadman P and T, validation.
- `firmware/`: watchdogs, timeouts, motor path.
- `core/contract.py`: renaming or removing messages or fields. Adding is fine.
- `ros/`: launch files and controller config.
- `deploy/`: service units.

## Never

- Import ROS (`rclpy`, message packages, `rosidl_runtime_py`) outside
  `adapters/ros/`, or at module level.
- Put I/O or ROS in `core/`.
- Build messages by hand (`{"type": ...}`) outside `core/contract.py`. Use
  `CONTRACT.encode` in Python and the builders in `@hhart/ui/core` in the
  browser.
- Send a command around the command port, or without its source.
- Let the browser talk to anything but the robot's WebSocket.

## Where things go

| Task | Where |
| --- | --- |
| Show a ROS topic (full ROS route) | One `CONTRACT.passthrough(...)` line, see [BINDING.md](BINDING.md) |
| Show a sensor (embedded route) | A device adapter and a tier 1 message |
| Add an operator button | A tier 1 `IN` message, then `hhart contract`. It shows as a generic form until it gets a view |
| Add a screen or panel | `apps/web/src/components/`, laid out in `App.tsx` |
