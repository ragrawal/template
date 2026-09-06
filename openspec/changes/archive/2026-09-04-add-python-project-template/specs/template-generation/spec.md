## Purpose

Defines the Copier answer-schema prompts and the templated project tree they render, so a developer can bootstrap a fully-tooled, installable Python project in a separate repository by running the Copier CLI against this repository.

## ADDED Requirements

### Requirement: Copier template source generates a new project
This repository MUST contain a single Copier template source (`copier.yml` plus a `template/` subdirectory) that, when run via the Copier CLI from a separate target repository, generates a new Python project scaffold there.

#### Scenario: Generate with prompts
- **WHEN** a developer runs the Copier CLI against this repository from a separate target directory and answers the prompts (`project_name`, `package_name`, `description`, `author_name`, `author_email`, `python_version`, `license`, `coverage_threshold`)
- **THEN** a new, independent project directory is created there with the standard folder structure, a dependency manifest, and dedicated configuration files for each development tool

#### Scenario: Only the template subtree is rendered
- **WHEN** Copier renders this repository's template
- **THEN** only files under `template/` are copied into the generated project; this repository's own `tests/`, root `pyproject.toml`, and top-level `.github/workflows/` are excluded

### Requirement: Generated project uses uv for dependency management
The generated project MUST use `uv` for installing, locking, and managing both runtime and development dependencies.

#### Scenario: Dependencies install cleanly
- **WHEN** a developer runs `uv sync` in a freshly generated project
- **THEN** all development tools (ruff, pyright, pytest, pytest-cov, poethepoet) install successfully with no additional manual configuration

### Requirement: Each development tool has its own dedicated configuration file
The generated project MUST include configuration for a linter/formatter (`ruff.toml`), a static type checker (`pyrightconfig.json`), a test framework (`pytest.ini`), and coverage enforcement (`.coveragerc`), each independently valid and usable without requiring changes to any other tool's configuration file.

#### Scenario: Editing one tool's config does not require editing another's
- **WHEN** a contributor edits `ruff.toml` in a generated project
- **THEN** ruff picks up the change without requiring any edit to `pyrightconfig.json`, `pytest.ini`, or `.coveragerc`

### Requirement: Generated project pins its Python version
The generated project MUST pin the Python version used for local development via a `.python-version` file, materialized immediately after generation.

#### Scenario: Python version is pinned after generation
- **WHEN** Copier finishes generating a project with `python_version` answered (default `3.12`)
- **THEN** the generated project contains a `.python-version` file matching that answer, produced by a post-generation `uv python pin` task

### Requirement: Generated project uses a src-layout installable package structure
This repository's template MUST generate projects intended as installable Python packages, using a `src`-layout folder structure and PEP 621 packaging metadata (via the `hatchling` build backend).

#### Scenario: Package is importable and buildable
- **WHEN** a project is generated with `package_name` answered
- **THEN** it contains `src/<package_name>/__init__.py` and `src/<package_name>/py.typed`, and its `pyproject.toml` declares a `hatchling` `[build-system]` and PEP 621 `[project]` metadata

### Requirement: Generated project includes foundational project-hygiene files
The generated project MUST include a `README.md`, a `LICENSE` file (rendered per the `license` answer), and a `.gitignore` as part of the standard scaffold.

#### Scenario: Hygiene files are present after generation
- **WHEN** a project is generated
- **THEN** `README.md`, `LICENSE`, and `.gitignore` exist at its root, with `LICENSE` matching the chosen `license` answer

### Requirement: Copier answer-schema changes preserve compatibility
Adding a new answer-schema key with a default MUST remain backward compatible; renaming or removing a key, or changing a default in a way that changes generated output for existing answers, MUST be accompanied by a Copier migration in `copier.yml`'s `_migrations` so `copier update` on existing generated projects does not silently break.

#### Scenario: Existing generated project updates safely
- **WHEN** a generated project runs `copier update` after the template's answer schema has changed
- **THEN** its prior answers are preserved, and any conflicting files are flagged for manual resolution rather than silently overwritten
