## Purpose

Defines the documentation and functional AI-assistant skill bundled into every generated project so an AI coding assistant can understand project conventions and invoke common actions without extra setup.

## ADDED Requirements

### Requirement: Bundled AI guidance documentation
Every generated project MUST include an `AGENTS.md` file documenting the project's conventions and its quality-check command.

#### Scenario: Assistant reads bundled guidance
- **WHEN** a developer opens a newly generated project with an AI coding assistant
- **THEN** `AGENTS.md` is present at the project root and documents the `uv run poe check` command

### Requirement: Bundled functional quality-check skill
Every generated project MUST include a functional, invocable assistant skill (`.claude/skills/run-quality-checks/SKILL.md`) that an AI coding assistant can invoke to run the project's quality-check task.

#### Scenario: Assistant invokes the skill to run checks
- **WHEN** a contributor asks their AI coding assistant to run the generated project's quality checks
- **THEN** the assistant identifies and invokes `.claude/skills/run-quality-checks`, which runs `uv run poe check`, using only the bundled guidance
