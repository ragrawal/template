## 1. Update the bundled (generated-project) AGENTS.md

- [x] 1.1 In `templates/python-project/AGENTS.md.jinja`'s "Coding Principles" section, add a bullet on test-driven development: structure tests so a human can add a new scenario easily, favoring `pytest.mark.parametrize` over one bespoke test function per case where the cases share shape.
- [x] 1.2 In the same section, add a bullet on algorithm complexity: before implementing non-trivial logic, briefly discuss the algorithm options considered and their time/space complexity rather than silently picking one.

## 2. Mirror the guidance into this repo's own AGENTS.md

- [x] 2.1 Add the same two bullets (from 1.1 and 1.2) to this repository's own root `AGENTS.md`, in its "Coding Principles" section, so the guidance also applies when working on this template repo itself.

## 3. Update this repo's regression suite

- [x] 3.1 In `tests/bdd/python_project_test/python_project_test.feature`, extend the "The generated project ships AI agent guidance and a quality-check skill" scenario with assertions that the generated `AGENTS.md` contains `pytest.mark.parametrize` and mentions time/space complexity, using the existing `the file "..." contains "..."` generic step; verify the scenario passes.

## 4. Full verification

- [x] 4.1 Run `uv run pytest` in this repository (this repo's actual CI check) and confirm it passes: 10 passed.
