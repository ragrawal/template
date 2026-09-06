## MODIFIED Requirements

### Requirement: PR-triggered quality workflow
Every generated project MUST include a GitHub Actions workflow that runs the project's `check` quality task, invoked with the `--full` flag, whenever a pull request is opened against that project's repository. Since `check` has no `CI`-environment-variable-based auto-detection of full vs. scoped behavior, the workflow MUST explicitly pass `--full` so it always exercises the complete, coverage-enforced check regardless of how the `check`/`test` tasks' own default (no-flag) behavior is defined.

#### Scenario: Opening a pull request triggers the workflow
- **WHEN** a pull request is opened against a generated project's repository
- **THEN** the bundled `.github/workflows/quality.yml` workflow runs, installing dependencies with `uv sync --locked` and then running `uv run poe check --full`, and reports its result on the pull request

#### Scenario: Workflow always runs the full check
- **WHEN** the bundled `.github/workflows/quality.yml` workflow runs `uv run poe check --full`
- **THEN** the format-check, type-check, and test steps all run against the entire project, with the test step running the complete suite with coverage enforced, because the workflow explicitly passes `--full`
