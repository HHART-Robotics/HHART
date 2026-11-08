# web

Operator UI (React, TypeScript). Panels come from `@hhart/ui` and are laid out
in `src/App.tsx`. Robot-specific code is in `src/robot/scene.ts` (3D model and
environment) and `src/core/` (pure view logic). New contract messages appear in
a generic panel without changes here.

From the repo root:

```text
pnpm install
pnpm dev           # http://localhost:3000, against robot1-bridge --port loopback
pnpm test
pnpm typecheck
pnpm build         # dist/, served on the robot by robot1-web.service
```
