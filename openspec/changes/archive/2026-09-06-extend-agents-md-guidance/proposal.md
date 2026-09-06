## Why

`AGENTS.md`'s "Coding Principles" section tells an AI assistant how to write code, but says nothing about how to write *tests* or how to reason about *algorithm choice*. Two gaps in particular keep resurfacing: tests get written as one bespoke assertion block per scenario instead of a parameterized table a human can extend by adding one row, and algorithmic tradeoffs (time/space complexity of the options considered) go undiscussed before an implementation is picked. This affects both this repo's own `AGENTS.md` and the `AGENTS.md.jinja` bundled into every generated downstream project, so the guidance should be added to both.

## What Changes

- Add a "Test-Driven Development" guidance item to `templates/python-project/AGENTS.md.jinja`'s Coding Principles section: tests should be structured so a human can add a new scenario easily, favoring `pytest.mark.parametrize` over one bespoke test function per case where the cases share shape.
- Add an "Algorithm complexity" guidance item to the same section: before implementing non-trivial logic, briefly discuss the algorithm options considered and their time/space complexity, rather than silently picking one.
- Mirror both additions into this repository's own root `AGENTS.md`, in the same "Coding Principles" section, so the guidance also applies to work on this template repository itself.

## Capabilities

### New Capabilities
(none)

### Modified Capabilities
- `ai-agent-guidance`: the "Bundled AI guidance documentation" requirement gains two new content obligations for the generated project's `AGENTS.md` (parameterized-test guidance, algorithm-complexity discussion guidance).

## Impact

- `templates/python-project/AGENTS.md.jinja` (Coding Principles section)
- `AGENTS.md` (this repository's own root file, Coding Principles section)
- `tests/bdd/python_project_test/python_project_test.feature` (new assertions that generated `AGENTS.md` contains the new guidance)
