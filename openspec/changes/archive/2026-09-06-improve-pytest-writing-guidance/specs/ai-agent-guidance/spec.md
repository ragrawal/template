## MODIFIED Requirements

### Requirement: Bundled AI guidance documentation
Every generated project MUST include an `AGENTS.md` file documenting the project's conventions and its quality-check command. Its "Coding Principles" section MUST also instruct the assistant to (1) structure tests so a human can add a new scenario easily, favoring `pytest.mark.parametrize` paired with `pytest.param(..., id="...")` so each case gets a descriptive, human-readable name instead of a positional index, and (2) discuss the algorithm options considered and their time/space complexity before implementing non-trivial logic.

#### Scenario: Assistant reads bundled guidance
- **WHEN** a developer opens a newly generated project with an AI coding assistant
- **THEN** `AGENTS.md` is present at the project root and documents the `uv run poe check` command

#### Scenario: Bundled guidance covers parameterized testing
- **WHEN** a developer opens a newly generated project's `AGENTS.md`
- **THEN** its Coding Principles section instructs the assistant to prefer `pytest.mark.parametrize` paired with `pytest.param(..., id="...")`, so a human can add a new test scenario by adding one named case rather than a new test function, and so a failing case is reported by its descriptive name rather than a positional index

#### Scenario: Bundled guidance covers algorithm complexity
- **WHEN** a developer opens a newly generated project's `AGENTS.md`
- **THEN** its Coding Principles section instructs the assistant to discuss the algorithm options considered and their time/space complexity before implementing non-trivial logic
