## ADDED Requirements

### Requirement: Lint step enforces Google-style documentation on public code
The `lint` task (and therefore `check`) MUST enforce that public modules, classes, and functions/methods carry a docstring conforming to the Google docstring convention. Test files under `tests/` MUST be exempt from this enforcement, since the project's testing convention (see `quality-check-task`'s sibling `ai-agent-guidance` capability) documents test intent through descriptive test names rather than docstrings. Private (leading-underscore) helpers are not required to carry docstrings under this ruleset's own defaults.

#### Scenario: A public class or function without a docstring fails lint
- **WHEN** a developer adds a public class or a public function/method under `src/` with no docstring and runs `uv run poe lint` (or `uv run poe check`)
- **THEN** the task reports a missing-docstring violation for that class or function and exits non-zero

#### Scenario: A docstring that violates the Google convention fails lint
- **WHEN** a developer adds a public class or function under `src/` with a docstring that does not conform to the Google docstring convention (for example, a malformed section header) and runs `uv run poe lint` (or `uv run poe check`)
- **THEN** the task reports a docstring-convention violation and exits non-zero

#### Scenario: Test files are exempt from docstring enforcement
- **WHEN** a developer adds a test function under `tests/` with no docstring and runs `uv run poe lint` (or `uv run poe check`)
- **THEN** the task does not report a missing-docstring violation for that test function

#### Scenario: Bundled scaffold passes the new lint rule out of the box
- **WHEN** a project is freshly generated (optionally including the `ml` overlay) with no further edits and `uv run poe check --full` is run
- **THEN** the lint step reports no missing-docstring violations
