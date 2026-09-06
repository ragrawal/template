## Purpose

Defines the single task-runner entry point bundled into every generated project that runs formatting, type-checking, and coverage-enforced tests together, reporting one overall pass/fail result.

## ADDED Requirements

### Requirement: Combined quality-check task
Every generated project MUST include a Poe the Poet task named `check` that runs, in sequence, a formatting check, a type-annotation check, and the test suite with coverage measurement, reporting a single overall pass/fail result.

#### Scenario: All checks pass
- **WHEN** a developer runs `uv run poe check` in a generated project with no violations
- **THEN** the format-check, type-check, and coverage-enforced test steps all run in order and the task exits `0`

#### Scenario: A violation fails the whole task
- **WHEN** a file has a formatting or type-annotation violation and the developer runs `uv run poe check`
- **THEN** the task reports which specific step failed and exits non-zero rather than silently passing

### Requirement: Individual quality sub-tasks are independently invocable
Every generated project MUST also expose `format`, `lint`, `typecheck`, and `test` as independently runnable Poe tasks, in addition to the combined `check` task.

#### Scenario: Run an individual sub-task
- **WHEN** a developer runs `uv run poe typecheck`
- **THEN** only `pyright` runs, independent of the `format`, `lint`, or `test` tasks

### Requirement: Test coverage threshold is enforced
The `test` task MUST enforce a minimum test-coverage threshold, read from `.coveragerc`'s `[report] fail_under` (default 80), failing the task when coverage falls below that threshold.

#### Scenario: Coverage below threshold fails the task
- **WHEN** `uv run poe test` runs and measured coverage is below the `.coveragerc` `fail_under` value
- **THEN** the task exits non-zero

#### Scenario: Coverage threshold is configurable at generation time
- **WHEN** a project is generated with a `coverage_threshold` answer other than the default
- **THEN** the generated `.coveragerc`'s `fail_under` matches that answer, and it is the single source of truth (not duplicated as a separate CLI flag)
