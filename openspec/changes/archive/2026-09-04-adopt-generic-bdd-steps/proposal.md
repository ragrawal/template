## Why

The current regression suite (`tests/features/template_generation.feature` + `tests/steps/test_template_generation.py`) uses business-language Gherkin phrasing (e.g. "a developer generates a project with default answers") backed by one bespoke pytest-bdd step function per scenario. This makes each new scenario require a new hand-written step, hides the exact command being run behind fixture code, and drifts from what a real downstream consumer actually types. Rewriting scenarios to show the literal, runnable CLI command in the step text — parsed by a small set of generic, reusable step definitions — makes the suite self-documenting and removes the need to write a new step function for most future scenarios.

## What Changes

- Rewrite `tests/features/template_generation.feature` so every `Given`/`When`/`Then` states a literal, runnable command or a concrete, checkable outcome (e.g. `When the user runs "uv tool run copier copy ... --defaults --trust"`, `Then the following files exist: AGENTS.md, pyproject.toml, ...`, `Then the command exits with code 0`, `Then the output contains "..."`).
- Replace the current one-function-per-scenario step definitions in `tests/steps/test_template_generation.py` with a small set of generic, reusable steps parameterized on the command string, a temporary-directory fixture, an exit code, a file list, or expected output text — reusable across scenarios without new Python code for most future scenarios.
- **BREAKING** for anyone relying on the current scenario wording or step function names in `tests/steps/test_template_generation.py` — both are being replaced.

## Capabilities

### New Capabilities
(none)

### Modified Capabilities
- `template-regression-testing`: the regression suite's scenarios and step definitions must use literal, runnable CLI commands and generic, reusable step definitions instead of bespoke per-scenario steps.

## Impact

- **Changed**: `tests/features/template_generation.feature`, `tests/steps/test_template_generation.py`.
- **Possibly changed**: `tests/conftest.py` fixtures, to the extent the new generic steps need a plain temporary-directory fixture rather than the current `generate_project`/`copy_template_source` helper fixtures.
- **Unaffected**: the shipped template itself (`copier.yml`, `template/`) and the push-triggered CI workflow (`.github/workflows/template-regression.yml`) — this only changes how the suite is written, not what it verifies.
