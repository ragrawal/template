## MODIFIED Requirements

### Requirement: Copier template source generates a new project
This repository MUST contain a single Copier template source at `templates/python-project/` (`templates/python-project/copier.yml` plus a `templates/python-project/template/` subdirectory) that, when run via the Copier CLI against `templates/python-project` from a separate target repository, generates a new Python project scaffold there.

#### Scenario: Generate with prompts
- **WHEN** a developer runs the Copier CLI against this repository's `templates/python-project` directory from a separate target directory and answers the prompts (`project_name`, `package_name`, `description`, `author_name`, `author_email`, `python_version`, `license`, `coverage_threshold`)
- **THEN** a new, independent project directory is created there with the standard folder structure, a dependency manifest, and dedicated configuration files for each development tool

#### Scenario: Only the template subtree is rendered
- **WHEN** Copier renders `templates/python-project`
- **THEN** only files under `templates/python-project/template/` are copied into the generated project; this repository's own `tests/`, root `pyproject.toml`, top-level `.github/workflows/`, and any other template under `templates/` are excluded
