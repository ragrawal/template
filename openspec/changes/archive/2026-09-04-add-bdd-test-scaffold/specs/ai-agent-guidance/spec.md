## ADDED Requirements

### Requirement: Bundled BDD-testing skill
Every generated project MUST include a functional, invocable assistant skill (`.claude/skills/write-bdd-tests/SKILL.md`) documenting the project's `tests/bdd/` directory structure, generic step vocabulary, action-module pattern, and the pytest-bdd step-registration convention, so an AI coding assistant can write correctly-wired BDD tests without rediscovering the registration gotcha.

#### Scenario: Assistant writes a new BDD scenario using the bundled skill
- **WHEN** a contributor asks their AI coding assistant to add a new BDD test to a generated project
- **THEN** the assistant identifies and invokes `.claude/skills/write-bdd-tests`, and follows its documented `tests/bdd/<feature>/` layout and action-module registration pattern, using only the bundled guidance
