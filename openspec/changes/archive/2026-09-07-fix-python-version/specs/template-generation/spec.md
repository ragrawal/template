## MODIFIED Requirements

### Requirement: Generated project pins its Python version
The generated project MUST pin the Python version used for local development via a `.python-version` file, materialized immediately after generation, written inside the generated `package_name` project directory (not the Copier destination path).

#### Scenario: Python version is pinned after generation
- **WHEN** Copier finishes generating a project with `python_version` answered (default `3.12`)
- **THEN** the generated project contains a `.python-version` file matching that answer, produced by a post-generation `uv python pin` task, located inside the `{{ package_name }}/` project directory rather than at the Copier destination root
