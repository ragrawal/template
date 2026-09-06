## Why

The `check` task's environment-aware behavior (local diff-scoping vs. CI/`--full` full run) is currently dispatched through `scripts/quality_check.py`, a standalone Python file that also recomputes changed files via `git diff`/merge-base to scope `ruff`/`pyright` reporting. That scoping logic is more machinery than the benefit justifies, and the maintainer wants the `check`/`test` tasks expressed natively in `poe_tasks.toml` (using poe's own args and shell/sequence task types) instead of an external script, with test-only scoping controlled by a single explicit flag rather than CI-environment detection.

## What Changes

- **BREAKING**: `scripts/quality_check.py` is removed. The `check` task is redefined natively in `poe_tasks.toml.jinja` as a `sequence` of `format-check`, `lint`, `typecheck`, `test`, with no external script.
- **BREAKING**: `format-check`, `lint`, and `typecheck` no longer scope to changed files under any circumstance (via `check` or standalone) — they always run against the entire project. The git-diff/merge-base changed-file computation is removed entirely.
- **BREAKING**: `check` no longer auto-detects the `CI` environment variable to decide full vs. scoped behavior. The only control is an explicit `--full` boolean arg on `check` (and on `test`), implemented as a poe task arg.
- `test` gains a `--full` boolean arg, implemented as a poe `shell` task: by default it runs `pytest --testmon -o addopts=` (coverage-based test-impact scoping, no coverage enforcement); with `--full` it runs plain `pytest` (whole suite, coverage enforced per `.coveragerc`). This is the same default/full split `test` already had when invoked through the old `check` script, now available on `test` itself, invoked directly or via `check`.
- `check --full` forwards `--full` to the `test` sub-task via poe's ref parameter expansion so the whole gate runs unscoped with coverage enforced; `check` (no flag) runs `format-check`/`lint`/`typecheck` full (as always) and `test` with testmon.
- The bundled GitHub Actions workflow (`quality.yml.jinja`) now explicitly runs `uv run poe check --full`, since `CI`-based auto-detection is removed and nothing else would make CI run the coverage-enforced full suite.
- Documentation (`README.md.jinja`, `AGENTS.md.jinja`, `.claude/skills/run-quality-checks/SKILL.md.jinja`) updated to describe the new default: format/lint/typecheck always full; `test`/`check` default to testmon-scoped tests, `--full` runs the complete suite with coverage enforced.

## Capabilities

### New Capabilities
(none)

### Modified Capabilities
- `quality-check-task`: `check`'s scoping mechanism changes from CI-env-var + git-diff-scoped format/lint/typecheck to: format/lint/typecheck always full, and only test selection (testmon vs. full) varies, controlled by an explicit `--full` poe arg (no environment detection). `test` invoked directly now also defaults to testmon-scoped rather than always full.
- `pr-quality-gate`: the bundled workflow must now explicitly pass `--full` to get the full, coverage-enforced check, since `check` no longer infers this from the `CI` environment variable.

## Impact

- `templates/python-project/poe_tasks.toml.jinja` — `check` becomes a `sequence` task with a `--full` arg forwarded to `test`; `test` becomes a `shell` task with its own `--full` arg branching on `testmon`; `format-check`/`lint`/`typecheck` unchanged (already full-project).
- `templates/python-project/scripts/quality_check.py` — deleted.
- `templates/python-project/.github/workflows/quality.yml.jinja` — `uv run poe check` becomes `uv run poe check --full`.
- `templates/python-project/README.md.jinja`, `AGENTS.md.jinja`, `.claude/skills/run-quality-checks/SKILL.md.jinja` — updated to describe the new default/`--full` behavior and drop references to diff-scoping and the `CI` env var.
- This repository's own regression suite (`tests/bdd/python_project_test/python_project_test.feature`) — the two scenarios that assert on `CI` env var behavior and scoped-output messages (`"Running full quality check"`, `"Running scoped quality check"`) no longer apply and need rewriting against the new `--full`-flag-only behavior.
- `templates/python-project/pyproject.toml.jinja` — no change; `pytest-testmon` dev dependency is retained.
