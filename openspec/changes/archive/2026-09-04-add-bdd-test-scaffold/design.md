## Context

See proposal.md - Why. This repo's own suite (under `tests/bdd/`, from `adopt-generic-bdd-steps`) proved out a working pytest-bdd pattern: action modules with `@given`/`@when`/`@then` on the functions themselves, registered via a wildcard import (no `__all__`) directly inside `conftest.py`, plus a minimal binding file per feature (`scenarios("<feature>.feature")` and nothing else). Generated projects currently ship only `tests/test_placeholder.py.jinja` (one plain pytest assertion) and have no `tests/__init__.py`, no `pytest-bdd` dependency, and no equivalent scaffold or skill.

## Goals / Non-Goals

**Goals:**
- Ship a `tests/bdd/` scaffold in every generated project that works immediately after generation, with no additional wiring.
- Reuse the exact registration pattern already proven in this repo, so the two codebases stay consistent and a contributor moving between them sees the same convention.
- Document the convention (including the non-obvious registration gotcha) in a bundled assistant skill, mirroring the existing `run-quality-checks` skill's style.

**Non-Goals:**
- Building out a large step-definition library speculatively - ship only the same small generic set this repo already uses (`shell.py`, `files.py`), trimmed to what makes sense with no pre-existing CLI to test.
- Wiring the example BDD scenario into any generation-time choice (e.g. a copier question to opt out) - it ships unconditionally, like the existing placeholder test.

## Decisions

**Trim the shipped action modules to what a brand-new project can exercise.**
`shell.py` ports directly (temporary directory, run command, exit-code/output assertions - these depend on nothing project-specific). `files.py` ports only `then_files_exist` and `then_file_contains`; this repo's `given_broken_template_source` and `then_quality_workflow_is_valid` are specific to testing *this template itself* and don't apply to a generated project. Alternative considered: ship no `files.py` and only `shell.py` until a project needs file assertions - rejected because file-existence/content checks are a near-universal need or the second thing to test after "does my CLI run," so shipping it up front avoids a Day 2 gotcha.

**The bundled example scenario exercises the generated package itself, not a placeholder shell command.**
`tests/bdd/example/example.feature` runs `python -c 'import {{ package_name }}; print({{ package_name }}.__version__)'` and asserts exit code 0 and the output contains `0.1.0`. This requires the feature file to be Jinja-rendered (`.jinja` suffix), unlike the plain, non-templated `test_example.py` binding file and action modules. Alternative considered: an unconditional `echo hello` scenario needing no templating - rejected because it would demonstrate the mechanics without proving the scaffold actually exercises the generated project, which is a stronger, still-safe example (no risk of recursively invoking `uv run poe check`, which would itself run pytest).

**Fix a latent packaging gap: add `tests/__init__.py` to the template.**
Verified by generating a project and running `uv run pytest`: without a root `tests/__init__.py`, pytest's import-mode package-root detection stops at `tests/` (since `tests/bdd/__init__.py` exists but `tests/__init__.py` doesn't), inserts `tests/` itself onto `sys.path`, and `from tests.bdd.actions.shell import *` in `conftest.py` fails with `ModuleNotFoundError: No module named 'tests'`. Adding an empty `tests/__init__.py` (matching this repo's own layout) fixes it; confirmed via a full generate-and-test run (`uv sync && uv run pytest -v` and `uv run poe check`, both green).

**Same conftest-wildcard-import registration pattern, `project_root` fixture instead of `repo_root`.**
The generated project's `tests/bdd/conftest.py` mirrors this repo's own almost exactly, but exposes a `project_root` fixture (the generated project's own root) rather than `repo_root` (which in this repo specifically means "the root of the template source"). No `clean_working_tree` fixture is shipped - that guarantee is specific to this repo regenerating itself and has no equivalent meaning for a downstream project's own tests.

**New skill file, not an addition to `run-quality-checks`.**
`write-bdd-tests` ships as its own skill (`.claude/skills/write-bdd-tests/SKILL.md.jinja`, plain content, no Jinja interpolation needed in the body) rather than folding BDD guidance into the existing quality-check skill, since they cover different, independently-invocable actions (running checks vs. writing a new test), matching how this repo now has two separate skills (`openspec-*` skills stay OpenSpec-specific, `write-bdd-tests` is new).

**This repo's own test collection needed scoping once the template shipped real `.py` files.**
Before this change, `template/` contained no plain `.py` files (only `.jinja`-suffixed ones, which pytest's default `test_*.py` collection pattern ignores). Adding `template/tests/bdd/conftest.py` and `template/tests/bdd/example/test_example.py` introduced the first ones, and this repo's `uv run pytest` had no `testpaths` restriction, so it started collecting them too - colliding on the dotted module name `tests.bdd.conftest` with this repo's own `tests/bdd/conftest.py` (`ImportPathMismatchError`) and failing to find `template/tests/bdd/example/example.feature` before it's Jinja-rendered (`FileNotFoundError`). Fixed by adding `[tool.pytest.ini_options]\ntestpaths = ["tests"]` to this repo's root `pyproject.toml`, scoping collection to this repo's own suite - the same restriction the generated project's own `pytest.ini` already applies to itself.

## Risks / Trade-offs

- **Two near-duplicate copies of `shell.py`/`files.py`/the skill content now exist (this repo's and the template's)** → accepted; the template's is deliberately a subset (no template-source-specific steps), and keeping them as plain files rather than a shared generated artifact keeps each one simple to read standalone. A future drift-check could diff the two if this becomes a maintenance problem.
- **Shipping a real dev dependency (`pytest-bdd`) increases install time and lockfile size for every generated project, even one that never writes a BDD test** → accepted per the proposal's explicit "a" scope decision; the existing `pytest`/`pytest-cov` dependencies already carry similar cost, and the scaffold provides immediate value (a runnable example) rather than dead weight.
