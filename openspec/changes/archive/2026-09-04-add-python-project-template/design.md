## Context

The behavior captured in the five new specs was originally designed and implemented under GitHub Spec Kit (`specs/001-python-project-template/plan.md` and `research.md`). That work is done and shipped; this design section preserves the technical rationale behind it so it isn't lost when the Spec Kit artifacts are retired, and covers the migration mechanics for the retirement itself. See proposal.md for why the migration is happening now.

## Goals / Non-Goals

**Goals:**
- Preserve the "why" behind already-shipped technical decisions (test framework, build backend, config-file layout, etc.) inside OpenSpec so future changes have that context.
- Cleanly retire the Spec Kit authoring tooling (`.specify/`, `specs/001-python-project-template/`, `.claude/skills/speckit-*/`) without touching the shipped template output (`copier.yml`, `template/`, `tests/`, `.github/workflows/`).

**Non-Goals:**
- Changing any shipped template behavior, file layout, or CI configuration as part of this migration.
- Re-litigating decisions already made and implemented (e.g., switching test frameworks or build backends) — this only records them.

## Decisions

- **Regression test framework: `pytest-bdd`.** Every generated project already standardizes on `pytest`; reusing it for this repository's own regression suite means one test runner and reuse of ordinary pytest fixtures alongside Gherkin scenarios. Alternative considered: `behave` (rejected — a second, disconnected test tool in a repository whose premise is tool consistency).
- **Regression suite drives the real `copier copy` CLI as a subprocess, not Copier's Python API.** Exercises the exact command a downstream consumer runs, catching CLI-surface regressions an in-process call would mask. Alternative considered: `copier.run_copy()` (rejected — diverges from actual user-invoked behavior across Copier versions).
- **Per-tool configuration stays in separate dedicated files** (`ruff.toml`, `pyrightconfig.json`, `pytest.ini`, `.coveragerc`, `poe_tasks.toml`, wired into `pyproject.toml` only via a one-line `[tool.poe] include` pointer). Alternative considered: consolidating into `[tool.*]` tables in `pyproject.toml` (rejected — violates the requirement that each tool's config be independently editable).
- **Build backend: `hatchling`.** Minimal-configuration, PEP 621-native, pairs well with `uv` and `src`-layout. Alternatives considered: `setuptools` (more legacy config surface), `pdm-backend`/`flit` (viable but less common default).
- **Python version pinning is a static prompt default plus a post-generation `uv python pin` task**, not dynamic "latest version" detection. Deterministic and reproducible across machines and CI. Alternative considered: dynamically detecting the latest CPython at generation time (rejected — fragile, network-dependent, non-reproducible).
- **Coverage threshold has one source of truth: `.coveragerc`'s `[report] fail_under`.** The `test` task relies on coverage.py's own enforcement rather than duplicating the number as a `pytest-cov` CLI flag, avoiding drift between two config points.
- **CI trigger semantics use each platform's defaults**: generated projects trigger on `pull_request: [opened, synchronize]`; this repository's own regression workflow triggers on unrestricted `push`. Chosen over hand-rolled equivalents to keep both workflows minimal.
- **Retirement approach for Spec Kit tooling: delete outright, rely on git history for recovery**, rather than archiving in place. The repository's own instruction set (AGENTS.md-level guidance) says this is now an OpenSpec repo; keeping dead `.specify/` scripts and `speckit-*` command skills around would leave two competing workflows discoverable side by side.

## Risks / Trade-offs

- Deleting `.claude/skills/speckit-*/` removes the `/speckit-*` slash commands immediately. Mitigation: git history retains every deleted file; nothing here is unrecoverable.
- The new OpenSpec specs describe behavior as observed in the current `template/` tree at migration time (verified by reading `template/`, `tests/`, and `.github/workflows/` directly, not by trusting the old spec's aspirational requirements). Mitigation: any spot where the old spec asserted something not actually shipped (e.g., a `CHANGELOG` file) was intentionally left out of the new specs rather than carried forward as fiction.
