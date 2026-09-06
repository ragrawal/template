# template-regression-testing Specification

## Purpose

Defines this repository's own behavior-driven regression suite and push-triggered CI workflow, which generate a real project from the current template and exercise its CLI commands so a template-breaking change is caught immediately rather than discovered later by a downstream consumer.

## Requirements

### Requirement: Regression suite exercises real CLI commands
This repository MUST include a `pytest-bdd` Given/When/Then regression suite that generates a real project from the current template source via the actual `copier copy` CLI (not an in-process API) and exercises that generated project's CLI commands (`uv sync`, `uv run poe check`). Scenario steps MUST state the literal, runnable command being executed (for example `uv tool run copier copy ... --defaults --trust`, `uv run poe check`) rather than paraphrased business language, and MUST be implemented by a small set of generic, reusable step definitions — parameterized on the command string, a file list, an exit code, or expected output text — rather than one bespoke step function per scenario. The suite MUST also cover the required-`package_name`-field failure mode described by the `template-generation` capability.

#### Scenario: Suite passes against a working template
- **WHEN** the regression suite runs against the current state of this repository's template
- **THEN** it generates a fresh project, runs `uv sync` and `uv run poe check` inside it, and reports an overall pass because both commands succeed

#### Scenario: Suite fails against a broken template
- **WHEN** a change to the template breaks project generation or breaks a generated project's CLI commands
- **THEN** the regression suite fails and its output identifies which generation step or generated-project command failed

#### Scenario: Scenario text shows the literal command
- **WHEN** a scenario needs to run a template-related CLI command
- **THEN** the scenario step text states the exact command being run (for example `the user runs "uv tool run copier copy ... --defaults --trust"`) instead of a paraphrased description of the action

#### Scenario: A new scenario reuses existing step definitions
- **WHEN** a new scenario is added that runs a command, checks that files exist, checks command output, or checks a command's exit code
- **THEN** it is expressible using the existing generic step definitions, without adding a new bespoke Python step function

#### Scenario: Missing package_name fails generation
- **WHEN** the suite runs `uv tool run copier copy ... --defaults --trust` omitting `-d package_name=...`
- **THEN** the command exits with a non-zero code and its output names the missing `package_name` question

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
