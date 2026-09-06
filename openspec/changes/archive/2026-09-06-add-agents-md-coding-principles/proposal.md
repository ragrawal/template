## Why

Generated projects' `AGENTS.md` currently documents only tooling and file-layout conventions — it says nothing about how an AI coding assistant should approach design decisions (where business logic lives, how to handle errors, when to add a dependency, how to name things). Without baseline guardrails, an assistant working in a generated project has no documented default for these recurring judgment calls. Separately, `AGENTS.md`'s "Running quality checks" section fully duplicates the step-by-step detail already documented in the bundled `run-quality-checks` skill, so the two drift independently whenever one is updated.

## What Changes

- Add a "Coding Principles" section to `AGENTS.md.jinja` documenting five baseline guardrails for an AI assistant working in a generated project: domain-model-first with thin controllers, DRY for business logic, fail fast/loud with no defensive programming, deliberate dependency choice (including recommending consolidation onto a more comprehensive library), and domain-language naming.
- Document that these are defaults, not strict rules — the assistant may deviate when a case genuinely warrants it, but must seek approval first rather than silently deviating.
- Trim the existing "Running quality checks" section in `AGENTS.md.jinja` to a short pointer to the bundled `run-quality-checks` skill instead of repeating its full step-by-step breakdown, removing the duplication between the two files.

## Capabilities

### Modified Capabilities
- `ai-agent-guidance`: the "Bundled AI guidance documentation" requirement gains the coding-principles content and the approval-before-deviation behavior, and is updated to require `AGENTS.md` to reference (not duplicate) the `run-quality-checks` skill's step-by-step detail.

## Impact

- `templates/python-project/AGENTS.md.jinja`: add "Coding Principles" section; shrink "Running quality checks" section.
- `tests/bdd/python_project_test/python_project_test.feature`: extend assertions to cover the new principles content bundled into generated projects.
