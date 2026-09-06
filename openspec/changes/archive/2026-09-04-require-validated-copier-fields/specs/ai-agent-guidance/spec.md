## MODIFIED Requirements

### Requirement: Bundled BDD-testing skill
Every generated project MUST include a functional, invocable assistant skill (`.claude/skills/write-bdd-tests/SKILL.md`) documenting the project's `tests/bdd/` directory structure, generic step vocabulary, action-module pattern, and the pytest-bdd step-registration convention, so an AI coding assistant can write correctly-wired BDD tests without rediscovering the registration gotcha. The skill's step-placement guidance MUST state a preference — not a strict rule — for generic, reusable step functions in the shared `tests/bdd/actions/` modules, while allowing a step that is genuinely specific to one feature and not reusable elsewhere to live directly in that feature's own step/binding file.

#### Scenario: Assistant writes a new BDD scenario using the bundled skill
- **WHEN** a contributor asks their AI coding assistant to add a new BDD test to a generated project
- **THEN** the assistant identifies and invokes `.claude/skills/write-bdd-tests`, and follows its documented `tests/bdd/<feature>/` layout and action-module registration pattern, using only the bundled guidance

#### Scenario: A feature-specific step is placed in its own file
- **WHEN** a contributor's AI coding assistant needs to write a step that is genuinely specific to one feature and would not be reusable elsewhere
- **THEN** the skill's guidance permits placing that step function directly in the feature's own step/binding file instead of forcing it into a shared action module
