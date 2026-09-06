## MODIFIED Requirements

### Requirement: Bundled AI guidance documentation
Every generated project MUST include an `AGENTS.md` file documenting the project's conventions and its quality-check command. Its "Coding Principles" section MUST also instruct the assistant to (1) structure tests so a human can add a new scenario easily, favoring `pytest.mark.parametrize` over one bespoke test function per case where the cases share shape, and (2) discuss the algorithm options considered and their time/space complexity before implementing non-trivial logic.

#### Scenario: Assistant reads bundled guidance
- **WHEN** a developer opens a newly generated project with an AI coding assistant
- **THEN** `AGENTS.md` is present at the project root and documents the `uv run poe check` command

#### Scenario: Bundled guidance covers parameterized testing
- **WHEN** a developer opens a newly generated project's `AGENTS.md`
- **THEN** its Coding Principles section instructs the assistant to prefer `pytest.mark.parametrize` so a human can add a new test scenario by adding one case rather than a new test function

#### Scenario: Bundled guidance covers algorithm complexity
- **WHEN** a developer opens a newly generated project's `AGENTS.md`
- **THEN** its Coding Principles section instructs the assistant to discuss the algorithm options considered and their time/space complexity before implementing non-trivial logic
