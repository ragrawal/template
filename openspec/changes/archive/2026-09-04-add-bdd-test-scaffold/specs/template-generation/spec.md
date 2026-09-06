## ADDED Requirements

### Requirement: Generated project includes a BDD test scaffold
Every generated project MUST include a working `tests/bdd/` pytest-bdd scaffold (generic, reusable action modules under `tests/bdd/actions/`, a `tests/bdd/conftest.py` that registers them, and an example feature demonstrating the convention) and the `pytest-bdd` dev dependency, so a downstream project can start writing behavior-driven tests immediately.

#### Scenario: BDD scaffold runs out of the box
- **WHEN** a developer generates a new project and runs `uv run pytest`
- **THEN** the bundled `tests/bdd/example` scenario is collected and passes, with no `StepDefinitionNotFoundError`
