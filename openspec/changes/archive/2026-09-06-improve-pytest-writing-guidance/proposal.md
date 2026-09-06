## Why

`AGENTS.md`'s "Coding Principles" section already tells an assistant to favor `pytest.mark.parametrize` over one bespoke test function per case, but it says nothing about *how* to label each case. Without an explicit case name, parametrized tests show up in `pytest` output as `test_foo[0]`, `test_foo[1]`, etc., which forces a human reviewer to cross-reference the parametrize table by position to understand what failed. `pytest.param(..., id="...")` solves this by attaching a human-readable name to each case, but assistants aren't currently told to use it.

## What Changes

- Extend the existing "Test-driven, easy to extend" bullet in `templates/python-project/AGENTS.md.jinja`'s Coding Principles section to instruct the assistant to pair `@pytest.mark.parametrize` with `pytest.param(..., id="...")` for each case, giving every parametrized case a descriptive, human-readable name instead of a positional index.
- Mirror the same wording into this repository's own root `AGENTS.md`, in the same "Coding Principles" section, so the guidance also applies to work on this template repository itself.
- Extend the "generated project ships AI agent guidance" BDD scenario to assert the generated `AGENTS.md` also mentions `pytest.param`.

## Capabilities

### Modified Capabilities
- `ai-agent-guidance`: the "Bundled AI guidance documentation" requirement's parameterized-test guidance now also requires naming each `pytest.param` case with an explicit `id`.

## Impact

- `templates/python-project/AGENTS.md.jinja` (Coding Principles section, "Test-driven, easy to extend" bullet)
- `AGENTS.md` (this repository's own root file, same bullet)
- `tests/bdd/python_project_test/python_project_test.feature` (new assertion that generated `AGENTS.md` mentions `pytest.param`)
