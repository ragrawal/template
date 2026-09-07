# template-generation Specification

## Purpose

Defines the Copier answer-schema prompts and the templated project tree they render, so a developer can bootstrap a fully-tooled, installable Python project in a separate repository by running the Copier CLI against this repository.

## Requirements

### Requirement: Copier template source generates a new project
This repository MUST contain a single Copier template source at `templates/python-project/` (`templates/python-project/copier.yml` plus a `templates/python-project/{{ package_name }}/` directory) that, when run via the Copier CLI against `templates/python-project` from a separate target repository, generates a new Python project scaffold there, nested under a folder named after the answered `package_name`.

#### Scenario: Generate with prompts
- **WHEN** a developer runs the Copier CLI against this repository's `templates/python-project` directory from a separate target directory `<dest>` and answers the prompts (`package_name`, `python_version`)
- **THEN** a new, independent project directory is created at `<dest>/<package_name>/` with the standard folder structure, a dependency manifest, and dedicated configuration files for each development tool

#### Scenario: Only the template subtree is rendered
- **WHEN** Copier renders `templates/python-project`
- **THEN** only files under `templates/python-project/{{ package_name }}/` are copied into the generated project, into a `<package_name>/` folder inside the destination; this repository's own `tests/`, root `pyproject.toml`, top-level `.github/workflows/`, and any other template under `templates/` are excluded

#### Scenario: Generating without package_name fails
- **WHEN** a developer runs the Copier CLI non-interactively (e.g. `--defaults`) without supplying `package_name`
- **THEN** Copier raises an error naming the missing question and does not generate a project

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
This repository's template MUST generate projects intended as installable Python packages, using a `src`-layout folder structure and PEP 621 packaging metadata (via the `hatchling` build backend), nested inside a top-level folder named after `package_name`.

#### Scenario: Package is importable and buildable
- **WHEN** a project is generated into destination `<dest>` with `package_name` answered
- **THEN** it contains `<dest>/<package_name>/src/<package_name>/__init__.py` and `<dest>/<package_name>/src/<package_name>/py.typed`, and `<dest>/<package_name>/pyproject.toml` declares a `hatchling` `[build-system]` and PEP 621 `[project]` metadata

### Requirement: Generated project includes foundational project-hygiene files
The generated project MUST include a `README.md` and a `.gitignore` as part of the standard scaffold. It MUST NOT include a `LICENSE` file, since the template no longer collects a license choice.

#### Scenario: Hygiene files are present after generation
- **WHEN** a project is generated
- **THEN** `README.md` and `.gitignore` exist at its root, and no `LICENSE` file is created

### Requirement: Generated project includes a BDD test scaffold
Every generated project MUST include a working `tests/bdd/` pytest-bdd scaffold (generic, reusable action modules under `tests/bdd/actions/`, a `tests/bdd/conftest.py` that registers them, and an example feature demonstrating the convention) and the `pytest-bdd` dev dependency, so a downstream project can start writing behavior-driven tests immediately.

#### Scenario: BDD scaffold runs out of the box
- **WHEN** a developer generates a new project and runs `uv run pytest`
- **THEN** the bundled `tests/bdd/example` scenario is collected and passes, with no `StepDefinitionNotFoundError`

### Requirement: Copier answer-schema changes preserve compatibility
Adding a new answer-schema key with a default MUST remain backward compatible; renaming or removing a key, or changing a default in a way that changes generated output for existing answers, MUST be accompanied by a Copier migration in `copier.yml`'s `_migrations` so `copier update` on existing generated projects does not silently break.

#### Scenario: Existing generated project updates safely
- **WHEN** a generated project runs `copier update` after the template's answer schema has changed
- **THEN** its prior answers are preserved, and any conflicting files are flagged for manual resolution rather than silently overwritten

### Requirement: Removed answers take a fixed value in generated output
Since `project_name`, `description`, `author_name`, `author_email`, `license`, and `coverage_threshold` are no longer prompted, the template MUST still produce valid output for the places that used to reference them: every place that rendered `project_name` (README heading, `AGENTS.md`, bundled skill docs) MUST render the literal `package_name` value instead; `pyproject.toml`'s `description` and `authors` fields MUST both be omitted entirely (an author entry with neither a `name` nor an `email` fails the `hatchling` build backend's validation, and both fields are optional under PEP 621); no `LICENSE` file or `[project.license]` table is generated; and the generated `.coveragerc` MUST enforce a fixed coverage threshold of `80`.

#### Scenario: Project name mirrors the package name
- **WHEN** a project is generated with `package_name=demo`
- **THEN** `README.md`'s top-level heading reads `# demo`

#### Scenario: pyproject.toml has no description, license, or authors metadata
- **WHEN** a project is generated
- **THEN** its `pyproject.toml` has no `description` key, no `[project.license]` table, and no `authors` key, and `uv sync` succeeds against it

#### Scenario: Coverage threshold is fixed regardless of answers supplied
- **WHEN** a project is generated
- **THEN** its `.coveragerc` enforces an `80`% coverage threshold, and Copier accepts no `coverage_threshold` answer (supplying `-d coverage_threshold=...` has no effect on generation)

### Requirement: Undefined template variables fail loudly
`copier.yml` MUST configure `_envops.undefined` so that any Jinja template variable left undefined during rendering raises an error instead of silently rendering as an empty string.

#### Scenario: Rendering with a missing variable errors
- **WHEN** a template file references a variable that has no value at render time (for example because the caller bypassed `copier.yml`'s question logic entirely)
- **THEN** rendering fails with an error rather than producing output containing a silently blank value
