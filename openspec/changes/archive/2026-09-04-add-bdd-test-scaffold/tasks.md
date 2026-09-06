## 1. Add the `pytest-bdd` dependency and packaging fix

- [x] 1.1 Add `pytest-bdd` to the `dev` dependency group in `template/pyproject.toml.jinja`; verify with `uv sync` in a freshly generated project showing `pytest-bdd` installed
- [x] 1.2 Add `template/tests/__init__.py` (empty) so `tests` is a regular importable package; verify by generating a project and confirming `tests/__init__.py` exists in the output

## 2. Scaffold `tests/bdd/` in the template

- [x] 2.1 Create `template/tests/bdd/actions/shell.py` (ported from this repo's `tests/bdd/actions/shell.py`: `given_temporary_directory`, `when_user_runs`, `when_user_runs_in_directory`, `then_command_exits_with_code`, `then_command_exits_nonzero`, `then_output_contains`) and `template/tests/bdd/actions/files.py` (`then_files_exist`, `then_file_contains` only - the template-source-specific steps from this repo's `files.py` are dropped); verify with `uv run python -c "import tests.bdd.actions.shell, tests.bdd.actions.files"` in a generated project
- [x] 2.2 Create `template/tests/bdd/conftest.py` registering both action modules via wildcard import (no `__all__`, no `pytest_plugins`) and exposing a `project_root` fixture; verify no `StepDefinitionNotFoundError` when running the example scenario
- [x] 2.3 Create `template/tests/bdd/example/example.feature.jinja` (one scenario: import the generated package and assert `__version__` via `python -c '...'`) and `template/tests/bdd/example/test_example.py` (binds the feature, nothing else); add `template/tests/bdd/__init__.py`, `template/tests/bdd/actions/__init__.py`, `template/tests/bdd/example/__init__.py`
- [x] 2.4 Generate a project (`uv tool run copier copy . <tmp> --trust --defaults -d project_name=... -d author_name=...`), run `uv sync && uv run pytest -v`, and confirm both the example BDD scenario and the existing placeholder test pass
- [x] 2.5 Run `uv run poe check` in the generated project and confirm formatting, type-checking, and coverage all pass with the new files present

## 3. Bundle the `write-bdd-tests` skill

- [x] 3.1 Create `.claude/skills/write-bdd-tests/SKILL.md` in this repo, documenting the `tests/bdd/` layout, generic step vocabulary, action-module pattern, and the pytest-bdd registration gotcha (and its fix)
- [x] 3.2 Create `template/.claude/skills/write-bdd-tests/SKILL.md.jinja` for generated projects, adapted to reference `project_root` and the shipped `tests/bdd/example/` feature instead of this repo's `repo_root`/`template_generation` feature; verify by generating a project and confirming the rendered file has no leftover Jinja syntax

## 4. Fix this repo's own test collection

- [x] 4.1 Discovered that once `template/tests/bdd/` contains real (non-`.jinja`) `.py` files, this repo's own `uv run pytest` (which had no `testpaths` restriction) started collecting them too, colliding on the dotted module name `tests.bdd.conftest` with this repo's own `tests/bdd/conftest.py` and failing with `ImportPathMismatchError`/`FileNotFoundError`. Added `[tool.pytest.ini_options]\ntestpaths = ["tests"]` to this repo's root `pyproject.toml` to scope collection to this repo's own suite; verified with `uv run pytest -v` reporting the same 6 `adopt-generic-bdd-steps` scenarios passing, with `template/tests/bdd/example` no longer collected

## 5. Validate

- [x] 5.1 Run `openspec validate add-bdd-test-scaffold --strict` and confirm it passes
- [x] 5.2 Run `openspec validate --specs` and confirm the existing main specs remain valid
