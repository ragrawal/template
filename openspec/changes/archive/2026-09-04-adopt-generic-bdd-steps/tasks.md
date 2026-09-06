## 1. Generic step definitions

- [x] 1.1 Add a `Given a temporary directory` step and a `When the user runs "<command>"` step to `tests/steps/test_template_generation.py` (or a new shared steps module), resolving `{repo_root}`/`{tmp_dir}` placeholders and running via `shlex.split` + `subprocess.run` (no `shell=True`); verify by running `uv run pytest tests/ -k template_generation -v` and confirming the new steps are collected without errors
- [x] 1.2 Add a `Then the following files exist: <comma-separated list>` step and a `Then the output contains "<text>"` step, both operating on the temporary directory / last command result set up by 1.1; verify with a throwaway scenario that asserts a known file (e.g. `pyproject.toml`) exists after generation
- [x] 1.3 Add a `Then the command exits with code <n>` step for scenarios that must assert failure explicitly; verify with a throwaway scenario against the existing broken-ruff-config case

## 2. Rewrite the feature file

- [x] 2.1 Rewrite `tests/features/template_generation.feature` so every scenario uses literal `uv tool run copier copy ...` / `uv run poe check` command text and the generic steps from Group 1, preserving the intent of all 6 existing scenarios (default-answers generation, custom-answers generation, broken-template failure, per-task exit-code contract, quality workflow validity, AGENTS.md/skill presence); verify by inspecting the diff for readability and running `uv run pytest --collect-only` to confirm all scenarios still parse
- [x] 2.2 For the quality-workflow scenario's YAML trigger check, keep a small dedicated `Then` step as documented in design.md, ported from the current `then_quality_workflow_is_valid` function; the AGENTS.md/skill content checks are covered by the new generic `Then the file "<path>" contains "<text>"` step instead of dedicated functions (a stronger fit for "generic, reusable" than the design's fallback of porting both dedicated functions verbatim); verify these scenarios still pass individually

## 3. Update fixtures and remove dead code

- [x] 3.1 Update `tests/conftest.py`: keep `repo_root` and `clean_working_tree` as-is; remove `generate_project` and `copy_template_source` once nothing references them; verify with `uv tool run ruff check --select F401,F841 tests/` (this repo has no `ruff.toml` of its own, so the check is scoped to unused-import/unused-variable rules rather than the full default ruleset) reporting no unused-fixture or unused-import warnings
- [x] 3.2 Remove the now-unreplaced bespoke step functions from `tests/steps/test_template_generation.py` (`given_current_template_source`, `given_broken_template_source`, `when_generate_default`, `when_generate_custom`, `when_generate_broken`, `when_quality_check_attempted`, `then_dependencies_install_cleanly`, `then_quality_check_passes`, `then_quality_check_fails`, `then_failure_identifies_broken_step`, `then_each_poe_task_exits_zero`) once their scenarios are re-expressed with generic steps; verify with `uv run pytest --collect-only` reporting zero "step not found" / unused step errors

## 4. Validate the full suite

- [x] 4.1 Run `uv run pytest` end-to-end and confirm all scenarios pass against the current (working) template
- [x] 4.2 Confirm `git status --porcelain` in this repository is unchanged before/after the run (the `clean_working_tree` fixture enforces this automatically)
- [x] 4.3 Run `openspec validate adopt-generic-bdd-steps --strict` and confirm it passes

## 5. Co-locate the feature and step files; factor actions into shared modules

- [x] 5.1 Create `tests/actions/shell.py` and `tests/actions/files.py`, with `@given`/`@when`/`@then` applied directly on the action functions (`given_temporary_directory`, `when_user_runs`, `when_user_runs_in_directory`, `then_command_exits_with_code`, `then_command_exits_nonzero`, `then_output_contains` in `shell.py`; `given_broken_template_source`, `then_files_exist`, `then_file_contains`, `then_quality_workflow_is_valid` in `files.py`); verify with `uv run python -c "import tests.actions.shell, tests.actions.files"`
- [x] 5.2 Move `tests/features/template_generation.feature` and a rewritten, minimal `tests/steps/test_template_generation.py` into a single `tests/template_generation/` directory; the step file only calls `scenarios("template_generation.feature")`. Discovered that pytest-bdd's step decorators register each fixture into the module where the decorator is literally written (via frame inspection), so plain imports of the decorated functions do not register them with pytest; fixed by declaring `pytest_plugins = ["tests.actions.shell", "tests.actions.files"]` in `tests/conftest.py`. Verified with `uv run pytest --collect-only` reporting the same 6 scenarios and `uv run pytest -v` passing all 6 (an interim version without the plugin registration collected fine but failed all 6 at runtime with `StepDefinitionNotFoundError`, confirming the fix was necessary)
- [x] 5.3 Remove the now-empty `tests/features/` and `tests/steps/` directories; verify with `find tests -type d` showing only `tests/actions/` and `tests/template_generation/` alongside `conftest.py`
- [x] 5.4 Run `uv run pytest` end-to-end and confirm all 6 scenarios still pass after the reorganization

## 6. Move everything BDD-related under `tests/bdd/`; drop `pytest_plugins` for the proven wildcard-import pattern

- [x] 6.1 Move `tests/actions/` to `tests/bdd/actions/`, `tests/template_generation/` to `tests/bdd/template_generation/`, and `tests/conftest.py` to `tests/bdd/conftest.py`; add `tests/bdd/__init__.py`; verify with `find tests -type f`
- [x] 6.2 Checked `~/mlplatform/gml`'s equivalent `tests/bdd/<feature>/test_<feature>.py` + `tests/bdd/shared/steps/*.py` layout at the user's request: it registers shared steps via `from tests.bdd.shared.steps.X import *` (no `__all__`) directly inside `tests/bdd/conftest.py`, not `pytest_plugins`. Removed `__all__` from `tests/bdd/actions/shell.py`/`files.py` and replaced `pytest_plugins = [...]` in `tests/bdd/conftest.py` with `from tests.bdd.actions.files import *` / `from tests.bdd.actions.shell import *`; verify with `uv run pytest --collect-only` reporting the same 6 scenarios and `uv run pytest -v` passing all 6
- [x] 6.3 Run `uv tool run ruff check --select F401,F841 tests/` and confirm no unused-import/unused-variable warnings after the move
- [x] 6.4 Run `openspec validate adopt-generic-bdd-steps --strict` and confirm it still passes
