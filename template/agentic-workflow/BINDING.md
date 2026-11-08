# UI and contract

The UI only talks to the robot's WebSocket, using the contract in
`software/python/src/robot1/core/contract.py`. No ROS in the browser (Rule 1).

## Show a ROS topic (full ROS route)

Add `CONTRACT.passthrough(name, topic=..., ros_type=..., fields={...}, units={...}, max_hz=...)`
and run `hhart contract`. It appears in the generic panel.

## Show a value the UI depends on

1. Add a frozen dataclass with `@CONTRACT.message(name)`. Units go in the field
   name (`range_mm`) or `field(metadata={"unit": ...})`.
2. Publish it from the session with `CONTRACT.encode(...)`.
3. Run `hhart contract` and add a view.

## Add a command

1. Add a dataclass with `direction=IN`.
2. Handle it in the operator server, calling the command port with source
   `OPERATOR`.
3. Add a builder in `apps/web/src/core/`. The golden test checks it against the
   contract.

## Notes

- Views read from `decode` and send through command builders. No protocol code
  in views.
- Check a field exists in `describe` before reading it. Show a dash if not.
- Renames and removals bump `CONTRACT.version`.
