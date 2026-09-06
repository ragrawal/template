## MODIFIED Requirements

### Requirement: PR-triggered quality workflow
Every generated project MUST include a GitHub Actions workflow that runs the project's `check` quality task whenever a pull request is opened against that project's repository. The workflow MUST NOT need to pass any diff-scoping flag or otherwise opt out of local-only scoping behavior the `check` task may apply — it MUST always exercise the full, unscoped check.

#### Scenario: Opening a pull request triggers the workflow
- **WHEN** a pull request is opened against a generated project's repository
- **THEN** the bundled `.github/workflows/quality.yml` workflow runs, installing dependencies with `uv sync --locked` and then running `uv run poe check`, and reports its result on the pull request

#### Scenario: Workflow always runs the full check
- **WHEN** the bundled `.github/workflows/quality.yml` workflow runs `uv run poe check`, regardless of how many files changed in the pull request
- **THEN** the format-check, type-check, and test steps all run against the entire project, not scoped to the diff, because the workflow's environment has `CI` set

### Requirement: Workflow re-runs on subsequent pushes to an open PR
The bundled workflow MUST automatically re-run whenever new commits are pushed to an already-open pull request.

#### Scenario: Pushing a follow-up commit re-runs the workflow
- **WHEN** a contributor pushes an additional commit to an open pull request that has already been checked once
- **THEN** the workflow automatically re-runs and updates the reported result, with no manual trigger
