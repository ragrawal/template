## MODIFIED Requirements

### Requirement: Behavior-driven regression suite exercises real CLI commands
This repository MUST include a `pytest-bdd` Given/When/Then regression suite that generates a real project from the current template source via the actual `copier copy` CLI (not an in-process API) and exercises that generated project's CLI commands (`uv sync`, `uv run poe check`). Scenario steps MUST state the literal, runnable command being executed (for example `uv tool run copier copy ... --defaults --trust`, `uv run poe check`) rather than paraphrased business language, and MUST be implemented by a small set of generic, reusable step definitions — parameterized on the command string, a file list, an exit code, or expected output text — rather than one bespoke step function per scenario. The suite MUST also cover the required-answer-field and out-of-range-validator failure modes described by the `template-generation` capability.

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

#### Scenario: Missing a required field fails generation
- **WHEN** the suite runs `uv tool run copier copy ... --defaults --trust` omitting `-d` for a required field such as `project_name`
- **THEN** the command exits with a non-zero code and its output names the missing question

#### Scenario: Out-of-range coverage_threshold fails validation
- **WHEN** the suite runs `uv tool run copier copy ... --data coverage_threshold=150 --defaults --trust` (or another out-of-range value such as `-5`)
- **THEN** the command exits with a non-zero code and its output contains the `coverage_threshold` validator's error message
