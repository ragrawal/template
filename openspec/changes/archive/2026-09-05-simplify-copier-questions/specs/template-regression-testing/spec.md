## REMOVED Requirements

### Requirement: Behavior-driven regression suite exercises real CLI commands
**Reason**: One of this requirement's six scenarios, "Out-of-range coverage_threshold fails validation", exercised a Copier answer (`coverage_threshold`) that no longer exists once the schema shrinks to `package_name` and `python_version`, so there is no longer a validator for it to exercise. The remaining five scenarios (suite pass/fail, literal command text, generic step reuse, and the required-field failure — now phrased against `package_name` instead of `project_name`/`author_name`) carry forward unchanged in meaning under "Regression suite exercises real CLI commands".
**Migration**: None. The out-of-range scenario is dropped outright; every other scenario's behavior is preserved under the replacement requirement below.

## ADDED Requirements

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
