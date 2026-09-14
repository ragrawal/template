## MODIFIED Requirements

### Requirement: Bundled AI guidance documentation
Every generated project MUST include an `AGENTS.md` file documenting the project's conventions, a set of baseline coding-guideline principles for an AI coding assistant to follow, and a pointer to the project's quality-check command. `AGENTS.md` MUST reference the bundled `run-quality-checks` skill for the quality-check command's step-by-step detail rather than duplicating it. Its "Coding Principles" section MUST also instruct the assistant to (1) structure tests so a human can add a new scenario easily, favoring `pytest.mark.parametrize` paired with `pytest.param(..., id="...")` so each case gets a descriptive, human-readable name instead of a positional index, and (2) discuss the algorithm options considered and their time/space complexity before implementing non-trivial logic.

The coding-guideline principles MUST include, at minimum:
- **Domain-model-first, thin controllers**: identify key domain concepts and push validation and business logic onto domain objects — Pydantic for validation-heavy models, `dataclasses` for simpler value objects — keeping controllers/handlers/routes minimal and delegating to the domain layer.
- **DRY for business logic**: avoid duplicating logic; extract functions that each do one specific, meaningful thing.
- **Fail fast and loud, no defensive programming**: validate hard at domain-model construction/boundaries; never silently default or swallow errors downstream (for example, index into `os.environ[...]` rather than assume a default via `os.environ.get(...)`); trust an invariant once established rather than re-checking it everywhere downstream.
- **Deliberate dependency choice**: before writing a workaround for a library's limitation, check whether the library is being misused or whether a leaner option already exists; when adding a new dependency, evaluate whether a single more comprehensive library would replace the functionality of one or more existing dependencies, and if so recommend consolidating onto it and removing the superseded dependencies.
- **Domain-language naming**: name types, functions, and variables after the domain concepts they represent rather than generic or purely technical terms.
- **Document public classes and methods**: every public class and function/method must have a Google-style docstring describing its purpose, enforced by the bundled lint step's docstring rules (see `quality-check-task`); private (leading-underscore) helpers and test functions are exempt.
- **Self-documenting Pydantic models**: define every Pydantic `BaseModel` field via `Field(..., description="...")`, even when no other validation is needed, so the model's JSON schema documents itself.

These principles MUST be presented as defaults, not strict rules: the assistant may deviate from one when a case genuinely warrants it, but MUST seek the developer's approval before proceeding with that deviation rather than silently deviating.

#### Scenario: Assistant reads bundled guidance
- **WHEN** a developer opens a newly generated project with an AI coding assistant
- **THEN** `AGENTS.md` is present at the project root, documents the coding-guideline principles, and references the `run-quality-checks` skill rather than repeating its step-by-step detail

#### Scenario: Assistant applies the bundled coding-guideline principles by default
- **WHEN** an AI coding assistant makes a design decision in a generated project touching business-logic placement, error handling, dependency selection, naming, documentation, or Pydantic model field declarations
- **THEN** it applies the bundled `AGENTS.md` principles (domain-model-first with thin controllers, DRY, fail fast and loud, deliberate dependency choice, domain-language naming, documenting public classes/methods, self-documenting Pydantic models) by default

#### Scenario: Assistant seeks approval before deviating from a principle
- **WHEN** an AI coding assistant determines that a case genuinely warrants deviating from one of the bundled coding-guideline principles
- **THEN** it asks the developer for approval before proceeding with that deviation, rather than silently deviating

#### Scenario: Bundled guidance covers parameterized testing
- **WHEN** a developer opens a newly generated project's `AGENTS.md`
- **THEN** its Coding Principles section instructs the assistant to prefer `pytest.mark.parametrize` paired with `pytest.param(..., id="...")`, so a human can add a new test scenario by adding one named case rather than a new test function, and so a failing case is reported by its descriptive name rather than a positional index

#### Scenario: Bundled guidance covers algorithm complexity
- **WHEN** a developer opens a newly generated project's `AGENTS.md`
- **THEN** its Coding Principles section instructs the assistant to discuss the algorithm options considered and their time/space complexity before implementing non-trivial logic

#### Scenario: Bundled guidance covers documentation and Pydantic field conventions
- **WHEN** a developer opens a newly generated project's `AGENTS.md`
- **THEN** its Coding Principles section instructs the assistant to document every public class and method with a Google-style docstring (exempting private helpers and test functions) and to declare every Pydantic model field via `Field(..., description=...)`
