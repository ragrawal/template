## 1. Update the bundled (generated-project) AGENTS.md

- [x] 1.1 In `templates/python-project/AGENTS.md.jinja`'s "Coding Principles" section, extend the "Test-driven, easy to extend" bullet to also instruct pairing `@pytest.mark.parametrize` with `pytest.param(..., id="...")`, giving each case a descriptive, human-readable name instead of a positional index. Verify with `grep -c "pytest.param" templates/python-project/AGENTS.md.jinja` returning `1`.

## 2. Mirror the guidance into this repo's own AGENTS.md

- [x] 2.1 Apply the same bullet update (from 1.1) to this repository's own root `AGENTS.md`, in its "Coding Principles" section, so the guidance also applies when working on this template repo itself. Verify with `grep -c "pytest.param" AGENTS.md` returning `1`.

## 3. Update this repo's regression suite

- [x] 3.1 In `tests/bdd/python_project_test/python_project_test.feature`, add an assertion to the "The generated project ships AI agent guidance and a quality-check skill" scenario that the generated `AGENTS.md` contains `pytest.param`, using the existing `the file "..." contains "..."` generic step.

## 4. Full verification

- [x] 4.1 Run `uv run pytest` in this repository and confirm it passes.
- [x] 4.2 Run `openspec validate improve-pytest-writing-guidance --strict` and confirm it passes before archiving.
