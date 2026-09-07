## Purpose

This repository *is* a [Copier](https://copier.readthedocs.io/) template source for bootstrapping installable Python projects. Other, independent repositories run the Copier CLI against this repository to generate a fully-tooled project scaffold in their own tree. This repository also maintains its own regression-test suite that generates a real project from the current template and exercises its CLI commands, so template changes can't silently break downstream consumers.

## Tech Stack

- **Template engine**: Copier (`templates/python-project/`, `copier.yml` alongside the template content)
- **Dependency management**: `uv`, both for developing this repository and inside every generated project
- **Generated-project tooling**: `ruff` (lint + format), `pyright` (static type checking), `pytest` + `pytest-cov` (tests + coverage), Poe the Poet (task runner), `hatchling` (PEP 621 build backend, `src`-layout packages)
- **This repository's own tooling**: `pytest` + `pytest-bdd` (Given/When/Then regression suite)
- **CI**: GitHub Actions — both this repository's push-triggered regression workflow and each generated project's PR-triggered quality workflow
- **Spec workflow**: OpenSpec (migrated from GitHub Spec Kit)

## Project Conventions

### Code Style

Each development tool (lint/format, type-check, test, coverage, task runner) is configured in its own dedicated file rather than combined into shared `[tool.*]` tables in `pyproject.toml` — `ruff.toml`, `pyrightconfig.json`, `pytest.ini`, `.coveragerc`, `poe_tasks.toml` (wired into `pyproject.toml` via a single `[tool.poe] include` pointer). `pyproject.toml` itself is limited to packaging metadata, `[build-system]`, and `[tool.uv]`. This convention applies both to this repository's own root config and to every file rendered into a generated project.

### Architecture Patterns

The shipped deliverable (`templates/python-project/`) is kept fully separate from this repository's own development tooling (root `pyproject.toml`, `tests/`, top-level `.github/workflows/`) by living in its own directory tree — nothing under this repository's own `tests/` or top-level `.github/` leaks into template output. `copier.yml` has no `_subdirectory`, so Copier's default excludes (`copier.yml`, `__pycache__`, `.git`, etc.) apply automatically to everything else in `templates/python-project/`. Everything below `copier.yml` lives under a templated `templates/python-project/{{ package_name }}/` directory, so generated output always lands nested under a `<package_name>/` folder inside whatever destination is passed to `copier copy`, rather than directly in that destination.

### Testing Strategy

This repository's own regression suite (`tests/bdd/*.feature` + `tests/bdd/actions/`) is behavior-driven (`pytest-bdd`, Given/When/Then) and shells out to the real `copier copy` CLI as a subprocess — not Copier's internal Python API — so it exercises the exact command a downstream consumer runs. Each scenario generates a project into a disposable `tmp_path` and asserts the generated project's own CLI commands (`uv sync`, `uv run poe check`) succeed. Every run must leave this repository's working tree unchanged.

Generated projects enforce a minimum test-coverage threshold via `.coveragerc`'s `[report] fail_under` (default 80%), which is the single source of truth — not duplicated as a `pytest-cov` CLI flag.

### Git Workflow

Standard GitHub PR workflow. Generated projects ship their own PR-triggered quality workflow (`pull_request: opened, synchronize`); this repository's own regression workflow triggers on unrestricted `push` (any branch), independent of whether a PR is open.

## Domain Context

- **Template**: the Copier template source authored here.
- **Generated Project**: a distinct Python project, living in its own separate repository, produced by running Copier against this repository.
- **Quality-Check Task**: the single Poe the Poet `check` task bundled into every generated project (format-check → type-check → coverage-enforced test).
- **Template Regression Test Suite**: this repository's own `pytest-bdd` suite that guards the template itself.

## Important Constraints

- `copier update` on an existing generated project must preserve prior answers and flag conflicting files for manual resolution rather than silently overwriting them.
- Every regression suite run must leave this repository's own working tree unchanged.
- Adding a new Copier answer-schema key with a default is backward compatible; renaming/removing a key or changing a default's generated output requires a `copier.yml` `_migrations` entry.
- Must run unmodified on GitHub Actions hosted runners, with no secrets or extra infrastructure required.

## External Dependencies

- **Copier** — template rendering engine consumed via `uv tool run copier`.
- **uv** — Python version and dependency management, both for this repository and every generated project.
- **GitHub Actions** (`ubuntu-latest`) — CI for both this repository and generated projects.
