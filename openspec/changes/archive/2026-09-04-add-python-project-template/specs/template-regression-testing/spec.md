## Purpose

Defines this repository's own behavior-driven regression suite and push-triggered CI workflow, which generate a real project from the current template and exercise its CLI commands so a template-breaking change is caught immediately rather than discovered later by a downstream consumer.

## ADDED Requirements

### Requirement: Behavior-driven regression suite exercises real CLI commands
This repository MUST include a `pytest-bdd` Given/When/Then regression suite that generates a real project from the current template source via the actual `copier copy` CLI (not an in-process API) and exercises that generated project's CLI commands (`uv sync`, `uv run poe check`).

#### Scenario: Suite passes against a working template
- **WHEN** the regression suite runs against the current state of this repository's template
- **THEN** it generates a fresh project, runs `uv sync` and `uv run poe check` inside it, and reports an overall pass because both commands succeed

#### Scenario: Suite fails against a broken template
- **WHEN** a change to the template breaks project generation or breaks a generated project's CLI commands
- **THEN** the regression suite fails and its output identifies which generation step or generated-project command failed

### Requirement: Regression suite leaves this repository's working tree unchanged
Every regression suite run MUST generate its project into a disposable location and leave this repository's own working tree unchanged after the run completes.

#### Scenario: No stray artifacts after a run
- **WHEN** the regression suite completes, whether it passes or fails
- **THEN** `git status --porcelain` in this repository reports the same result as before the run started

### Requirement: Push-triggered regression workflow
This repository MUST include a GitHub Actions workflow that automatically runs the regression suite whenever a commit is pushed, independent of whether a pull request is open.

#### Scenario: Pushing a commit triggers the regression workflow
- **WHEN** a maintainer pushes a commit to any branch of this repository
- **THEN** `.github/workflows/template-regression.yml` runs, installing dependencies with `uv sync --locked` and then running `uv run pytest`, and reports its result
