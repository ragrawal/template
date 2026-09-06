## MODIFIED Requirements

### Requirement: Combined quality-check task
Every generated project MUST include a Poe the Poet task named `check` that runs a formatting check, a type-annotation check, and the test suite with coverage measurement, reporting a single overall pass/fail result. When run in an environment where the `CI` environment variable is set, or when invoked with an explicit `--full` flag, `check` MUST run these steps against the entire project, unscoped. Otherwise, `check` MUST scope the formatting check, the type-annotation check's reported diagnostics, and test selection to files changed relative to the current branch's merge-base with the default branch (falling back to uncommitted changes against `HEAD` if no such merge-base can be determined). If the project directory is not a git repository at all, `check` MUST run the full, unscoped check rather than silently skipping the formatting or type-check steps.

#### Scenario: All checks pass
- **WHEN** a developer runs `uv run poe check` in a generated project with no violations
- **THEN** the format-check, type-check, and coverage-enforced test steps all run in order and the task exits `0`

#### Scenario: All checks pass (full run)
- **WHEN** a developer runs `uv run poe check --full`, or `CI` is set, in a generated project with no violations
- **THEN** the format-check, type-check, and coverage-enforced test steps all run against the entire project in order and the task exits `0`

#### Scenario: A violation fails the whole task
- **WHEN** a file has a formatting or type-annotation violation and the developer runs `uv run poe check`
- **THEN** the task reports which specific step failed and exits non-zero rather than silently passing

#### Scenario: Local run scopes to changed files
- **WHEN** a developer runs `uv run poe check` locally (no `CI` environment variable set, no `--full` flag) with uncommitted or branch changes touching a subset of files
- **THEN** the formatting check and type-check reporting apply only to files changed relative to the branch's merge-base, and the test step selects only tests affected by that diff

#### Scenario: CI run always runs the full check
- **WHEN** `uv run poe check` runs in an environment where the `CI` environment variable is set
- **THEN** the task runs the formatting check, type-check, and test suite against the entire project, identical to passing `--full`, regardless of how large or small the diff is

#### Scenario: No git repository present
- **WHEN** a developer runs `uv run poe check` in a project directory that is not (or not yet) a git repository
- **THEN** the task runs the full, unscoped formatting check, type-check, and test suite rather than skipping any step

### Requirement: Individual quality sub-tasks are independently invocable
Every generated project MUST also expose `format`, `lint`, `typecheck`, and `test` as independently runnable Poe tasks, in addition to the combined `check` task. Running a sub-task directly (not via `check`) MUST always operate on the entire project, unscoped.

#### Scenario: Run an individual sub-task
- **WHEN** a developer runs `uv run poe typecheck`
- **THEN** only `pyright` runs, against the entire project, independent of the `format`, `lint`, or `test` tasks

### Requirement: Test coverage threshold is enforced
The `test` task MUST enforce a minimum test-coverage threshold, read from `.coveragerc`'s `[report] fail_under` (default 80), failing the task when coverage falls below that threshold. This threshold enforcement applies to a full-project test run (`uv run poe test`, or `check`/`check --full` when running unscoped); a diff-scoped test run performed as part of a local `check` invocation is not required to enforce the threshold, since it deliberately runs a subset of tests.

#### Scenario: Coverage below threshold fails the task
- **WHEN** `uv run poe test` runs and measured coverage is below the `.coveragerc` `fail_under` value
- **THEN** the task exits non-zero

#### Scenario: Coverage threshold is configurable at generation time
- **WHEN** a project is generated with a `coverage_threshold` answer other than the default
- **THEN** the generated `.coveragerc`'s `fail_under` matches that answer, and it is the single source of truth (not duplicated as a separate CLI flag)

## ADDED Requirements

### Requirement: Test selection uses coverage-based impact analysis
When `check` runs in scoped (non-full) mode, the test step MUST select tests using coverage-based dependency tracking (`pytest-testmon`) rather than matching test files by name alone, so that a change to a shared dependency reruns every test that exercises it, not only tests residing in changed files. The local test-impact cache MUST be excluded from version control. When no cache exists (for example, immediately after cloning), the test step MUST fall back to running the full test suite once to build it.

#### Scenario: Change to a shared utility reruns dependent tests
- **WHEN** a developer modifies a source file that is imported by tests in multiple test files, and runs `uv run poe check` locally
- **THEN** all tests whose coverage recorded a dependency on the changed lines run, even if their test file was not itself modified

#### Scenario: No impact-analysis cache is present
- **WHEN** a developer runs `uv run poe check` locally in a freshly cloned repository with no test-impact cache present
- **THEN** the test step runs the full test suite once and builds the cache for subsequent scoped runs
