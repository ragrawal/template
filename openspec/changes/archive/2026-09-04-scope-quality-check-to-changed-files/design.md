## Context

Every generated project bundles a Poe the Poet `check` task (`format-check` -> `typecheck` -> `test`, see `openspec/specs/quality-check-task/spec.md`) and a GitHub Actions workflow that runs that same task on every PR (`openspec/specs/pr-quality-gate/spec.md`). Both currently always operate on the whole repository. `poe`'s TOML task format (`sequence`, `cmd`) has no conditional branching, so any environment-dependent behavior needs a small script rather than pure declarative config.

## Goals / Non-Goals

**Goals:**
- Local `uv run poe check` scopes format/lint/typecheck reporting and test selection to the current branch's diff, by default.
- CI's invocation of `uv run poe check` continues to run the full, unscoped check with zero changes to the workflow file, by relying on the `CI` env var GitHub Actions already sets.
- A developer can force a full local run with an explicit flag.
- Individual sub-tasks (`format`, `lint`, `typecheck`, `test`) remain independently invocable per the existing spec, and default to their current (full-repo) behavior when run directly — only the combined `check` task changes behavior.

**Non-Goals:**
- Not changing what CI reports or how PRs are gated — the full check still runs there, unchanged.
- Not attempting cross-file lint analysis improvements; ruff's selected rule set (E/F/I/UP/B) is already per-file safe to scope.
- Not solving type-check downstream-breakage detection — pyright scoped to changed files still won't catch every case a full run would; that gap is accepted locally because CI's full run is the actual gate.

## Decisions

**1. Environment auto-detection over a required manual flag.**
`check` decides scope by checking the `CI` env var (set automatically by GitHub Actions, and a de facto standard other CI systems set too) rather than requiring the CI workflow to pass `--full`. This means the workflow file (`quality.yml.jinja`) needs no change and can't silently regress by someone editing it later. An explicit `--full` flag is still supported so a developer can force the complete gate locally. Alternative considered: two separate poe tasks (`check` / `check-ci`) — rejected because it still relies on the workflow author remembering to call the right one, the exact fragility this design avoids.

**2. Dispatch through a small script, not nested poe sequences.**
`check` becomes a `cmd`/`script` task that invokes a helper (e.g. `scripts/quality_check.py`, exact path/name finalized in tasks.md) which: computes whether to run scoped or full, computes the changed-file set via `git diff --name-only <merge-base-with-default-branch>`, and shells out to `ruff format --check`, `ruff check`, `pyright`, and `pytest` with the appropriate arguments. This keeps `poe_tasks.toml.jinja` simple and puts branching logic somewhere it can actually branch.

**3. Pyright is scoped by passing explicit file paths, not by skipping it.**
Pyright's CLI still loads and resolves the whole project's import graph when given explicit file arguments — it only limits which files it *reports* diagnostics for. This is safer than a naive "skip pyright for unchanged files" approach, though it still won't flag breakage introduced in an unchanged downstream file (accepted per Non-Goals; CI's full run is the actual backstop).

**4. Test scoping via `pytest-testmon`, not filename matching.**
`pytest-testmon` uses coverage data to know which tests actually exercise which lines, so a change to a shared util correctly reruns everything that depends on it — not just tests whose own file changed. This pairs naturally with the coverage enforcement this template already has (`.coveragerc.jinja`). `.testmondata` (the local cache) is gitignored; a fresh clone's first run has no cache and testmon runs the full suite once to build it, then incremental runs are fast. `--full` also bypasses testmon and runs the complete suite.

**5. No change needed to the regression suite's expectations.**
This repository's own regression suite (`tests/bdd/`) generates a project and runs `uv run poe check` as a subprocess inside a GitHub Actions job (`template-regression.yml`). Since `CI=true` is already set in that job and subprocess calls inherit the parent environment by default, the regression suite will exercise the full-check path without any special-casing — it validates the same behavior downstream consumers' CI gets.

## Risks / Trade-offs

- [Local scoped run gives false confidence that a change is safe] -> Mitigated by CI always running the full check before merge; scoped local runs are a speed optimization for iteration, not a replacement for the gate.
- [`pytest-testmon`'s cache can go stale or get corrupted across branch switches] -> `--full` flag provides an escape hatch; documented in generated `AGENTS.md`/README as "run `poe check --full` if results look wrong."
- [New dev dependency (`pytest-testmon`) increases template surface area] -> Accepted; it directly composes with the coverage enforcement already in place rather than introducing a parallel selection mechanism.
- [Diff base for "changed files" is ambiguous outside a PR branch workflow (e.g., no upstream tracking branch configured)] -> Fall back to diffing against `HEAD` (uncommitted changes) if no merge-base with a default branch can be determined; exact fallback order finalized during implementation.
