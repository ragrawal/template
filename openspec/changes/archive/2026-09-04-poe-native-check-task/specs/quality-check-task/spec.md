## MODIFIED Requirements

### Requirement: Combined quality-check task
Every generated project MUST include a Poe the Poet task named `check` that runs a formatting check, a type-annotation check, and the test suite, reporting a single overall pass/fail result. `check` MUST accept an explicit `--full` flag, implemented as a native poe task argument (not environment-variable detection or an external script). Passing `--full` to `check` MUST forward `--full` to the `test` sub-task so the complete test suite runs with coverage enforced; omitting `--full` MUST run `test` with its default testmon-scoped behavior. The `format-check`, `lint`, and `typecheck` steps within `check` MUST always run against the entire project regardless of whether `--full` is passed — `check` has no diff-scoping and no `CI`-environment-variable-based branching for these steps.

#### Scenario: All checks pass
- **WHEN** a developer runs `uv run poe check` in a generated project with no violations
- **THEN** the format-check, type-check, and test steps all run in order against the entire project (test using testmon-based selection) and the task exits `0`

#### Scenario: All checks pass (full run)
- **WHEN** a developer runs `uv run poe check --full` in a generated project with no violations
- **THEN** the format-check, type-check, and test steps all run against the entire project, with the test step running the complete suite with coverage enforced, and the task exits `0`

#### Scenario: A violation fails the whole task
- **WHEN** a file has a formatting or type-annotation violation and the developer runs `uv run poe check`
- **THEN** the task reports which specific step failed and exits non-zero rather than silently passing

#### Scenario: Local run scopes to changed files
- **WHEN** a developer runs `uv run poe check` locally with uncommitted or branch changes touching only a subset of files
- **THEN** the format-check and type-check steps still run against the entire project, not scoped to the diff — `check` has no file-scoping behavior for these steps, regardless of how small the change is

#### Scenario: CI run always runs the full check
- **WHEN** `uv run poe check` (without `--full`) runs in an environment where the `CI` environment variable is set
- **THEN** the task behaves identically to running outside CI — the `CI` environment variable has no effect, and the test step still uses testmon-scoped selection unless `--full` is explicitly passed

#### Scenario: No git repository present
- **WHEN** a developer runs `uv run poe check` in a project directory that is not (or not yet) a git repository
- **THEN** the task runs identically to running inside a git repository — `check` performs no git-based detection, so format-check, type-check, and (testmon-scoped, cache-building) test all run normally

### Requirement: Individual quality sub-tasks are independently invocable
Every generated project MUST also expose `format`, `lint`, `typecheck`, and `test` as independently runnable Poe tasks, in addition to the combined `check` task. Running `format`, `lint`, or `typecheck` directly (not via `check`) MUST always operate on the entire project, unscoped, identical to their behavior within `check`. Running `test` directly MUST default to the same testmon-scoped selection `check` uses by default, and MUST accept the same `--full` flag `check` accepts to run the complete suite with coverage enforced instead.

#### Scenario: Run an individual sub-task
- **WHEN** a developer runs `uv run poe typecheck`
- **THEN** only `pyright` runs, against the entire project, independent of the `format`, `lint`, or `test` tasks

#### Scenario: Run test directly with default scoping
- **WHEN** a developer runs `uv run poe test` directly (not via `check`)
- **THEN** the test step runs with testmon-based test selection, the same default `check` uses when `--full` is omitted

#### Scenario: Run test directly with --full
- **WHEN** a developer runs `uv run poe test --full` directly (not via `check`)
- **THEN** the complete test suite runs with coverage enforced, the same behavior `check --full` produces for its test step

### Requirement: Test coverage threshold is enforced
The `test` task MUST enforce a minimum test-coverage threshold, read from `.coveragerc`'s `[report] fail_under` (default 80), failing the task when coverage falls below that threshold, when running the full suite (`uv run poe test --full`, or `check --full`). A testmon-scoped `test` run — the default for `test` and for `check` when `--full` is omitted — is not required to enforce the threshold, since it deliberately runs a subset of tests.

#### Scenario: Coverage below threshold fails the task
- **WHEN** `uv run poe test --full` runs and measured coverage is below the `.coveragerc` `fail_under` value
- **THEN** the task exits non-zero

#### Scenario: Coverage threshold is configurable at generation time
- **WHEN** a project is generated with a `coverage_threshold` answer other than the default
- **THEN** the generated `.coveragerc`'s `fail_under` matches that answer, and it is the single source of truth (not duplicated as a separate CLI flag)

### Requirement: Test selection uses coverage-based impact analysis
The `test` task MUST select tests using coverage-based dependency tracking (`pytest-testmon`) by default — whether invoked directly (`uv run poe test`) or via `check` without `--full` — rather than matching test files by name or scoping via a git diff, so that a change to a shared dependency reruns every test that exercises it, not only tests residing in changed files. Passing `--full` to `test` (directly, or forwarded from `check --full`) MUST bypass testmon and run the complete suite instead. The local test-impact cache MUST be excluded from version control. When no cache exists (for example, immediately after cloning), the test step MUST fall back to running the full test suite once to build it.

#### Scenario: Change to a shared utility reruns dependent tests
- **WHEN** a developer modifies a source file that is imported by tests in multiple test files, and runs `uv run poe test` (or `uv run poe check` without `--full`)
- **THEN** all tests whose coverage recorded a dependency on the changed lines run, even if their test file was not itself modified

#### Scenario: No impact-analysis cache is present
- **WHEN** a developer runs `uv run poe test` (or `uv run poe check` without `--full`) in a freshly cloned repository with no test-impact cache present
- **THEN** the test step runs the full test suite once and builds the cache for subsequent scoped runs
