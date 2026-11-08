# Contributing

Open issues and PRs in this repo (HHART-Robotics/HHART). HHART-Python and
HHART-UI are read-only mirrors and don't take issues or PRs.

Search existing issues before opening one. Report security issues privately,
see [SECURITY.md](SECURITY.md).

## Scope

- `python/`: things every robot needs. Stdlib only.
- `ui/`: the standard operator UI.
- `template/`: has to stay a working robot that passes its own rules without
  hardware or ROS.
- Code for one robot goes in that robot's repo.

One stack per tier: Python (uv) for the robot, ROS 2 Jazzy, React +
TypeScript (pnpm) for the UI and API, PlatformIO for firmware. PRs adding a
second option for a tier won't be merged.

The rules in `template/README.md` match the paper word for word. Rule changes
start as an issue and only ship in a major release.

## Making a change

1. Branch from `main` as `<type>/<scope>-<summary>`, e.g.
   `fix/fitness-relative-imports`.
2. Add a test that fails without your change.
3. Run everything:

   ```text
   pytest python/tests
   pytest template/software/python/tests
   hhart check template
   pnpm install && pnpm typecheck && pnpm test
   cd template/software/firmware/robot1 && uvx --from platformio pio test -e native
   ```

4. Add a line under `## [Unreleased]` in `CHANGELOG.md`.
5. Commit with `git commit -s` and open a PR. PRs are squash-merged, so the
   title has to be a conventional commit.

Style: ASCII only. Comments explain why, not what. `core/` stays pure (no I/O,
ROS, browser or Node APIs), the checks enforce it. UI code uses `@hhart/ui`
tokens, no new colours. Firmware: no dynamic allocation, loop never blocks.

## Commits

[Conventional Commits](https://www.conventionalcommits.org):
`<type>(<scope>): <summary>`, lowercase, imperative, no full stop.

- Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`,
  `ci`, `chore`, `revert`.
- Scopes: `arbitration`, `contract`, `operator`, `fitness`, `cli`, `ports`,
  `ui`, `template`, `web`, `api`, `firmware`, `ros`, `deploy`, `ci`, `docs`,
  `repo`.
- Breaking changes: `!` after the scope and a `BREAKING CHANGE:` footer.

## Licence

HHART is Apache-2.0. Contributions are under the same licence (section 5), no CLA.
Signing off (`git commit -s`) certifies the
[DCO](https://developercertificate.org). Third-party code has to be under a
compatible licence (Apache-2.0, MIT, BSD, ISC, Zlib) with its notice kept. No
GPL. Generated code is your responsibility like anything else you submit.

## Releasing

From `main`:

1. Bump the version in `python/pyproject.toml`, `python/package.xml`,
   `python/src/hhart/__init__.py`, `ui/package.json` and `CITATION.cff`.
   `tests/test_cli.py` checks they match.
2. Rename `## [Unreleased]` in `CHANGELOG.md` to the version.
3. Commit `chore(repo): release vX.Y.Z`, then
   `git tag -a vX.Y.Z -m vX.Y.Z && git push origin vX.Y.Z`.

The release workflow checks the versions, builds, publishes to PyPI and the
GitHub release, and updates the mirrors. Tags are never moved.
