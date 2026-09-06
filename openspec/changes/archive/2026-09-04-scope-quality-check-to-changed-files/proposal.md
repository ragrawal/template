## Why

Generated projects run the full `check` task (format, lint, typecheck, coverage-enforced tests) on every local invocation, even for a one-line change. Since CI already re-validates the entire repo on every PR, local runs can be scoped to what actually changed, making local iteration much faster without weakening the guarantee that a full, unscoped check gates every PR.

## What Changes

- `poe check` becomes environment-aware: when run locally (no `CI` env var set), it scopes formatting, linting, and type-check reporting to files changed against the branch's merge-base, and scopes tests to those actually affected by the diff.
- When `CI` is set (GitHub Actions sets this automatically) or an explicit `--full` flag is passed, `check` runs the full, unscoped checks exactly as it does today. No change is needed to the bundled CI workflow file itself for this to take effect.
- Test scoping uses `pytest-testmon` (new dev dependency) rather than naive git-diff filename matching, so tests are selected by actual coverage-tracked dependency on changed lines, not just by which test file was touched.
- `.testmondata` (testmon's local cache) is gitignored; the first run after a fresh clone falls back to a full test run to build the cache.
- A `--full` override remains available so a developer can run the complete gate locally before pushing.

## Capabilities

### New Capabilities
(none)

### Modified Capabilities
- `quality-check-task`: the `check` task's behavior changes from "always full-repo" to "scoped to the diff by default, full when `CI` is set or `--full` is passed"; adds coverage-based test selection via `pytest-testmon`.
- `pr-quality-gate`: adds an explicit requirement that the bundled CI workflow always exercises the full, unscoped check regardless of the new local scoping behavior, since it runs with `CI` set.

## Impact

- `templates/python-project/poe_tasks.toml.jinja` — `check` (and possibly `test`) task definitions change to dispatch through a small helper script instead of a plain sequence.
- `templates/python-project/pyproject.toml.jinja` — add `pytest-testmon` to the dev dependency group.
- `templates/python-project/.gitignore.jinja` — ignore `.testmondata`.
- New template file for the dispatch helper (e.g. `templates/python-project/scripts/check.py.jinja` or similar — exact location decided in design.md).
- `templates/python-project/.github/workflows/quality.yml.jinja` — no functional change expected; confirmed in design.md.
- This repository's own regression suite (`tests/bdd/`) — no new requirement, but worth a pass to confirm it still exercises the full-check path (it runs `uv run poe check` inside a GitHub Actions job, which inherits `CI=true`).
