## Purpose

Defines the GitHub Actions workflow bundled into every generated project that automatically enforces the quality-check task on pull requests, without a maintainer manually triggering it.

## ADDED Requirements

### Requirement: PR-triggered quality workflow
Every generated project MUST include a GitHub Actions workflow that runs the project's `check` quality task whenever a pull request is opened against that project's repository.

#### Scenario: Opening a pull request triggers the workflow
- **WHEN** a pull request is opened against a generated project's repository
- **THEN** the bundled `.github/workflows/quality.yml` workflow runs, installing dependencies with `uv sync --locked` and then running `uv run poe check`, and reports its result on the pull request

### Requirement: Workflow re-runs on subsequent pushes to an open PR
The bundled workflow MUST automatically re-run whenever new commits are pushed to an already-open pull request.

#### Scenario: Pushing a follow-up commit re-runs the workflow
- **WHEN** a contributor pushes an additional commit to an open pull request that has already been checked once
- **THEN** the workflow automatically re-runs and updates the reported result, with no manual trigger
