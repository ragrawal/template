## Context

`check` currently dispatches to `scripts/quality_check.py` (a plain `cmd = "python scripts/quality_check.py"` task, see `openspec/specs/quality-check-task/spec.md`), which detects `CI`/`--full`, computes changed files via `git diff`/merge-base, and scopes `ruff format --check`, `ruff check`, and `pyright` to that file set, always running `test` with `pytest --testmon -o addopts=` in scoped mode. See `proposal.md` - Why for the motivation to remove this script. The template's dev dependency group already includes `poethepoet` and `pytest-testmon`; nothing changes there.

## Goals / Non-Goals

**Goals:**
- Express `check`'s and `test`'s branching entirely as native `poe_tasks.toml` constructs (task `args`, `shell`, `sequence`, `ref` parameter expansion) — no `.py`/`.sh` file on disk.
- `check` and `test` both accept a `--full` boolean flag with identical semantics: full pytest with coverage enforced vs. the testmon-scoped default.
- `check --full` forwards `--full` to its `test` sub-task so one flag controls the whole gate.
- The bundled CI workflow keeps getting the full, coverage-enforced check on every PR.

**Non-Goals:**
- Not preserving diff-scoped `format-check`/`lint`/`typecheck` reporting — per the user's direction, those three steps always run against the whole project now, so no git-diff or merge-base logic is needed anywhere in the template.
- Not changing the coverage threshold mechanism (`.coveragerc`'s `fail_under`) or the `pytest-testmon` dependency itself.
- Not handling Windows `cmd.exe`/PowerShell shells specially — see Risks.

## Decisions

**1. `test` becomes a `shell` task with a `--full` boolean arg.**
```toml
[tasks.test]
help = "Run pytest; testmon-scoped by default, pass --full to run the whole suite with coverage enforced"
args = [{ name = "full", options = ["--full"], type = "boolean" }]
shell = """
if [ -n "${full:-}" ]; then
  pytest
else
  pytest --testmon -o addopts=
fi
"""
```
A poe boolean arg is exported to the shell environment as `"True"` when set, unset otherwise, so `[ -n "${full:-}" ]` is the correct truthiness check. `shell` (not `cmd`) is required because `cmd` tasks have no conditional branching — this is the one place actual shell logic is needed, and it's inline TOML, not a separate file. Alternative considered: a `switch` task keyed on `full`; rejected as more verbose than a two-line `if` for a single boolean.

**2. `check` becomes a `sequence` task that forwards `--full` to `test` via `ref` parameter expansion.**
```toml
[tasks.check]
help = "Run format-check, lint, typecheck, and test (pass --full to run the full suite with coverage enforced)"
args = [{ name = "full", options = ["--full"], type = "boolean" }]
sequence = [
  { ref = "format-check" },
  { ref = "lint" },
  { ref = "typecheck" },
  { ref = "test ${full:+--full}" },
]
```
`ref` supports `:+`/`:-` parameter expansion (per poethepoet's args reference), so `${full:+--full}` expands to `--full` when `check`'s `full` arg is set, and to nothing otherwise — `test` then applies its own default. This keeps `check`'s only branching decision (testmon vs. full) inside `test` itself, so the two tasks can never disagree about what `--full` means.

**3. Drop `CI`-environment-variable detection and git-diff scoping entirely — no replacement logic.**
Since `format-check`/`lint`/`typecheck` always run full (Non-Goals), and `test`'s scoping is now controlled solely by the explicit `--full` arg, there is nothing left that needs to know whether it's running in CI. This removes the `is_git_repo()` fallback requirement too (previously: "if not a git repo, run the full check") — `pytest-testmon` itself already handles a missing `.testmondata` cache by running the full suite once and building it, with no template-side special-casing needed.

**4. The bundled CI workflow explicitly passes `--full`.**
```yaml
- name: Run quality checks
  run: uv run poe check --full
```
Previously the workflow needed no change because `check` inferred `--full` behavior from `CI` (set automatically by GitHub Actions). With that auto-detection removed, the workflow must say `--full` explicitly to get the coverage-enforced full suite — otherwise a PR's `check` run would silently use testmon-scoped test selection. Per the proposal's Impact section, `pr-quality-gate`'s spec is updated accordingly.

**5. Delete `scripts/quality_check.py` outright; no deprecation shim.**
Nothing else in the template references it once `poe_tasks.toml.jinja` no longer calls it (confirmed via repo-wide grep in proposal research). No migration shim is needed since this is a copier template, not a library with external callers — each newly generated project simply gets the new `poe_tasks.toml` from here on.

## Risks / Trade-offs

- [Local `check`/`format`/`lint`/`typecheck` invocations always run full-project now, losing the fast, changed-files-only local iteration loop the prior scoping change (`2026-09-04-scope-quality-check-to-changed-files`) introduced] → Accepted per explicit user direction; `test`'s testmon default still keeps the test step itself fast, which was called out as the part worth keeping.
- [`shell` tasks require a POSIX-ish shell interpreter (`sh`/`bash`/`zsh`), unlike `cmd` tasks which poe runs without invoking a shell at all] → Acceptable: CI runs on `ubuntu-latest`, and local dev on macOS/Linux has one of these by default; not a regression since the template has no existing Windows-native (`cmd.exe`/PowerShell) support to preserve.
- [A developer or CI author could forget `--full` and get a weaker, testmon-scoped PR gate] → Mitigated by making the CI workflow file itself the single place `--full` is set (Decision 4), and documenting the flag prominently in `README.md.jinja`/`AGENTS.md.jinja`/the `run-quality-checks` skill.
