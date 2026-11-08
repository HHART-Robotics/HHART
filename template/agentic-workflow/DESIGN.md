# Operator UI design

Guidelines from MICROPIRO's operator UI.

## User

A field technician running one robot, often outdoors, on a laptop or tablet.
They're also handling the tether, so they aren't always watching the screen.
They need to:

- notice a lost link, a tip or a stuck robot without reading anything
- record observations with the robot's position

## Guidelines

- Only measurements, controls and labels. Nothing decorative.
- Quiet when normal, obvious when not.
- Colour only where it means something: greys for structure, one accent for
  clickable things, three status colours (ok, warning, fault), data colours
  kept separate.
- Never colour alone. Status colours get a text label, data colours a legend.
- Unknown is a dash, never zero. Stale values are dimmed. Faults use the
  robot's own text.
- The robot's main reading (e.g. distance along a pipe) is always visible and
  largest.
- One main element per screen.

## Always visible

- Stop, one click or key away. Release next to it after an operator stop.
- Connection state.
- Active faults.

## Input

- Keyboard drives (WASD, arrows) alongside on-screen controls, but not while
  typing in a field.
- Touch targets at least 32 px for drive controls, 24 px elsewhere.

## Accessibility

- Contrast at least 4.5:1 for values, 3:1 for labels.
- Visible focus on every control.
- Respect `prefers-reduced-motion`. Don't animate numbers.
