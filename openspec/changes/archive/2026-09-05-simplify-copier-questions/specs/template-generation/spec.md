## MODIFIED Requirements

### Requirement: Copier template source generates a new project
This repository MUST contain a single Copier template source at `templates/python-project/` (`templates/python-project/copier.yml` plus a `templates/python-project/template/` subdirectory) that, when run via the Copier CLI against `templates/python-project` from a separate target repository, generates a new Python project scaffold there.

#### Scenario: Generate with prompts
- **WHEN** a developer runs the Copier CLI against this repository's `templates/python-project` directory from a separate target directory and answers the prompts (`package_name`, `python_version`)
- **THEN** a new, independent project directory is created there with the standard folder structure, a dependency manifest, and dedicated configuration files for each development tool

#### Scenario: Only the template subtree is rendered
- **WHEN** Copier renders `templates/python-project`
- **THEN** only files under `templates/python-project/template/` are copied into the generated project; this repository's own `tests/`, root `pyproject.toml`, top-level `.github/workflows/`, and any other template under `templates/` are excluded

#### Scenario: Generating without package_name fails
- **WHEN** a developer runs the Copier CLI non-interactively (e.g. `--defaults`) without supplying `package_name`
- **THEN** Copier raises an error naming the missing question and does not generate a project

### Requirement: Generated project includes foundational project-hygiene files
The generated project MUST include a `README.md` and a `.gitignore` as part of the standard scaffold. It MUST NOT include a `LICENSE` file, since the template no longer collects a license choice.

#### Scenario: Hygiene files are present after generation
- **WHEN** a project is generated
- **THEN** `README.md` and `.gitignore` exist at its root, and no `LICENSE` file is created

## REMOVED Requirements

### Requirement: Validated answer fields are required
**Reason**: The answer schema shrank to `package_name` and `python_version` only, so the rule enumerating which of several validated fields need a `default:` no longer has multiple fields to enumerate. `package_name`'s required-field behavior is preserved as a scenario on "Copier template source generates a new project" instead of its own requirement.
**Migration**: None. `package_name` remains required with no `default:`; see the "Generating without package_name fails" scenario on "Copier template source generates a new project".

## ADDED Requirements

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
