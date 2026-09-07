## MODIFIED Requirements

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

### Requirement: Generated project uses a src-layout installable package structure
This repository's template MUST generate projects intended as installable Python packages, using a `src`-layout folder structure and PEP 621 packaging metadata (via the `hatchling` build backend), nested inside a top-level folder named after `package_name`.

#### Scenario: Package is importable and buildable
- **WHEN** a project is generated into destination `<dest>` with `package_name` answered
- **THEN** it contains `<dest>/<package_name>/src/<package_name>/__init__.py` and `<dest>/<package_name>/src/<package_name>/py.typed`, and `<dest>/<package_name>/pyproject.toml` declares a `hatchling` `[build-system]` and PEP 621 `[project]` metadata
