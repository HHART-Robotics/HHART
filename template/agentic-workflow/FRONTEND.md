# Operator UI

How to build this robot's UI in `software/apps/web/`. The standard panels come
from `@hhart/ui`. A robot only changes its 3D slots, its own views and which
messages they show. Improve shared panels in HHART's `ui/`, not here.

## Read first

1. `software/CONTRACT.md`: every message, with units.
2. [DESIGN.md](DESIGN.md)
3. [BINDING.md](BINDING.md)
4. `@hhart/ui`'s README

## Provided

| Part | From `@hhart/ui` | Robot supplies |
| --- | --- | --- |
| Top bar | `TopBar` | Extra fields as children, e.g. pipe size |
| Drive | `DrivePanel` | Nothing for a diff drive |
| Faults | `FaultsPanel` | Nothing |
| Scene | `SceneView` | `RobotModel` and `Environment` in `src/robot/scene.ts` |
| Readouts | `PoseHud` | Main reading and readouts from `src/core/` |
| Camera | `CameraPanel` | Frame, if the contract has one. Otherwise delete it |
| Research tools | `Drawer`, `CapabilityPanel` | Tabs and notes |
| Other messages | `MessagePanel`, `CommandForm` | Nothing until it gets its own view |

## Plan

From CONTRACT.md and DESIGN.md, list:

- the operator's tasks (drive to the next joint, mark a defect)
- the messages and commands each task uses
- the robot's main reading
- what a fault or lost link looks like on each screen

If a task needs a message the contract doesn't have, a person adds it to
`contract.py` first (see [AGENTS.md](AGENTS.md)).

## Where code goes

| What | Where | Tested by |
| --- | --- | --- |
| Derived values, readouts | `src/core/*.ts`, pure, imports only itself and `@hhart/ui/core` | `pnpm test` against `contract.golden.json` |
| Model and environment | `src/robot/scene.ts`, metres, REP 103, `base_link` at origin | By eye against `robot1-bridge --port loopback` |
| Views | `src/components/*.tsx`, kit classes and tokens only | `pnpm typecheck`, `pnpm build` |
| Layout | `src/App.tsx`, and `OWN_VIEWS` in `src/core/robot.ts` | `pnpm build` |

New functions in `src/core/` need tests. `architecture.test.ts` fails if a core
imports anything else or uses a browser API.

## Must stay true

- Stop on every screen, on the keyboard (Space), Release next to it after a
  stop.
- Letting go of a drive control stops the robot. Held drives resend every
  `KEEPALIVE_MS`.
- Connection state, route and active faults always visible.
- Unknown is a dash, never zero. Stale is dimmed.
- No ROS names in front of the operator (Rule 1), except in the drawer's
  research tab. The browser only talks to the robot's WebSocket.
- Messages without a view still appear in a generic panel.

## Verify

```text
cd software/apps/web
pnpm test && pnpm typecheck && pnpm build
cd ../../python
robot1-bridge --port loopback   # then pnpm dev and drive from the page
```
