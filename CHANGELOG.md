# Changelog

## [Unreleased]

## [0.1.1] - 2026-11-08

- vite 8, vitest 5 and @vitejs/plugin-react 6 in `ui/` and the template's apps. Fixes 29
  Dependabot alerts in vite, vitest, esbuild and tinypool.
- Release workflow pushes the mirrors with `MIRROR_TOKEN` (the v0.1.0 mirror push failed).
  Mirroring is now its own workflow, `mirror.yml`, and can be rerun for a tag from the
  Actions tab.
- GitHub Actions on their Node 24 versions.
- `hhart new` and the template point to the README's Run section (was Use).

## [0.1.0] - 2026-11-08

First release.
