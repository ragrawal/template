## Context

See proposal.md - Why. Today's suite (`tests/features/template_generation.feature` + `tests/steps/test_template_generation.py`) has 6 scenarios, each backed by its own `@given`/`@when`/`@then` function keyed to that scenario's exact wording. `tests/conftest.py` currently provides higher-level fixtures (`generate_project`, `copy_template_source`, `repo_root`) that wrap `copier copy` via `sys.executable -m copier copy ...` (an in-process module invocation), plus an autouse `clean_working_tree` fixture that snapshots `git status --porcelain` before/after every test. This repository's own README documents the real end-user command as `uv tool run copier copy <src> <dst>`.

## Goals / Non-Goals

**Goals:**
- Every `Given`/`When`/`Then` in `template_generation.feature` shows a literal, runnable shell command or a concrete, checkable outcome (file list, output substring, exit code) instead of paraphrased business language.
- Replace the 14 bespoke step functions with a small, fixed set of generic step definitions that any future scenario can reuse without new Python code.
- Preserve all existing behavior coverage (the 6 current scenarios' intent) and the "leaves working tree unchanged" guarantee.

**Non-Goals:**
- Changing what the suite verifies (the underlying capability contract in `quality-check-task`, `pr-quality-gate`, and `ai-agent-guidance` specs is unaffected).
- Changing the push-triggered CI workflow (`.github/workflows/template-regression.yml`).
- Achieving 100% generic coverage for every conceivable future scenario — a handful of steps needing custom assertions (e.g. YAML-trigger inspection) remain acceptable as small, dedicated steps if they can't be expressed generically.

## Decisions

**Literal command text uses `uv tool run copier copy`, not `python -m copier copy`.**
The README documents `uv tool run copier copy <src> <dst>` as the real command a downstream consumer runs. Using this text in scenarios makes the suite's own documentation double as living, runnable proof that the documented command works. Alternative considered: keep the current internal `sys.executable -m copier copy` invocation for speed/isolation reasons — rejected because it would make the scenario text diverge from what a reader executes by hand, defeating the goal of literal, copy-pasteable commands. The underlying fixture may still shell out however is fastest/most reliable in CI, as long as the *scenario step text* is the literal, documented command a user would actually type.

**Generic step vocabulary.**
Adopt four reusable step shapes, each backed by one small function:
- `Given a temporary directory` — provisions an isolated `tmp_path`-backed working directory (already implicit via pytest-bdd's `tmp_path`; made an explicit named fixture step so scenarios can state it).
- `When the user runs "<command>"` — runs a shell command (string, with `{tmp_dir}`-style placeholders resolved against the scenario's temporary directory and repo root), capturing exit code and combined output for later `Then` steps.
- `Then the following files exist: <comma-separated list>` — asserts each named path exists relative to the temporary directory.
- `Then the output contains "<text>"` — asserts substring presence in the last command's combined stdout+stderr.
- `Then the command exits with code <n>` — asserts the last command's exit code (used where a scenario needs to assert failure explicitly rather than infer it from a following command's success).

Alternative considered: one generic `run("<command>")` step plus custom Python assertions per scenario (as `pytest`-only tests, not BDD `Then` steps) — rejected because it would abandon Gherkin's readability for the assertion half of each scenario, which is exactly what the user asked to keep declarative.

**Chained commands within one scenario share state via the temporary directory, not fixture return values.**
`When ... and runs "uv run poe check"` (a second command against the same generated project) is expressed as two `When the user runs "<command>"` steps in sequence, both scoped to the same temporary directory fixture. The last command's result (exit code + output) is what subsequent `Then` steps check. This avoids introducing per-scenario `target_fixture` plumbing for multi-command scenarios.

**Existing fixtures in `tests/conftest.py` are trimmed, not fully replaced.**
`clean_working_tree` (working-tree-unchanged guarantee) and `repo_root` are kept as-is. `generate_project` and `copy_template_source` are replaced by the new generic step implementation, which resolves `{repo_root}`/`{tmp_dir}` placeholders in command strings itself rather than going through a bespoke Python wrapper per generation flavor (default answers, custom answers, broken template). The "broken template" scenario becomes: copy the template to a temp dir with a shell command (or a small setup step), corrupt one file, then run the literal `uv tool run copier copy <broken-temp-dir> <dst> ...` command like any other scenario.

**Coverage of all 6 current scenarios is preserved by re-expressing each with the new vocabulary**, not by dropping any. The "quality workflow is valid YAML" and "AGENTS.md/skill reference the quality-check command" scenarios still need a *content* check beyond plain substring matching (parsing YAML, checking nested keys) — these keep a small dedicated `Then` step per check they need, since forcing YAML-structure assertions into "output contains" would be a weaker check than the current one. This is a deliberate, narrow exception to "no bespoke steps," scoped to structural/content assertions that a generic substring-or-file-existence step can't express.

**All BDD test code lives under `tests/bdd/`; `@given`/`@when`/`@then` decorators live directly on the action functions in shared modules.**
`tests/features/template_generation.feature` and `tests/steps/test_template_generation.py` move into `tests/bdd/template_generation/` (the feature file and its step file live side by side, matching pytest-bdd's default of resolving a `scenarios(...)` path relative to the calling step module). The step-decorated functions themselves (command execution steps, file/content assertion steps, the broken-template setup step) move into `tests/bdd/actions/shell.py` and `tests/bdd/actions/files.py`, grouped by concern, with `@given`/`@when`/`@then` applied directly at their definition site — not re-declared as separate wrapper functions. `tests/bdd/template_generation/test_template_generation.py` becomes minimal: just `scenarios("template_generation.feature")`. `tests/conftest.py` (fixtures unrelated to any one feature: `repo_root`, `clean_working_tree`) moves to `tests/bdd/conftest.py` since, in this repository, all of `tests/` is the BDD suite.

This required working around a pytest-bdd internal: `@given`/`@when`/`@then` register each step's fixture by frame-inspecting the caller and injecting it into *that call site's own module namespace* (`pytest_bdd/steps.py`'s `step()` uses `get_caller_module_locals`), not into the function object itself. A plain `import` of a step-decorated function elsewhere therefore does not make pytest discover it — the fixture stays registered only under `tests.bdd.actions.shell`/`tests.bdd.actions.files`'s own module dict, invisible to a test module that only imports names from it. This was confirmed by testing: a version that imported the functions into the step file (via `from ... import *` with an explicit `__all__` restricting the export to the plain function names) collected all 6 scenarios successfully but failed all 6 at runtime with `StepDefinitionNotFoundError`.

Two fixes were tried. The first, `pytest_plugins = ["tests.actions.shell", "tests.actions.files"]` in `tests/conftest.py`, worked but was replaced after checking how `~/mlplatform/gml` (an existing, larger repo with the identical `tests/bdd/<feature>/test_<feature>.py` + `tests/bdd/shared/steps/*.py` layout) solves the same problem: it does **not** use `pytest_plugins` — its own `tests/bdd/conftest.py` comment notes pytest forbids `pytest_plugins` in a non-root conftest, so that mechanism doesn't generalize to a project with more than one conftest.py. Instead it does `from tests.bdd.shared.steps.cli_steps import *` (no `__all__`) directly inside `tests/bdd/conftest.py`. This is the actual fix: pytest-bdd's frame injection adds the real fixture under a mangled name (e.g. `pytestbdd_stepdef_given_...`) into the defining module's namespace; since that name has no leading underscore, an `import *` **without an `__all__`** pulls it along too, and because `conftest.py` is a module pytest scans directly for fixtures (regardless of level in the tree), the mangled fixture becomes visible to every test under it. This is pytest-bdd's own documented sharing pattern, works with any number of conftest.py files, and needed no plugin registration — so the final implementation follows it and drops both the `__all__` restriction and `pytest_plugins`. Alternative considered: keep the action-module logic in plain helper functions and re-declare thin `@given`/`@when`/`@then` wrappers in the step file — rejected per explicit follow-up direction that the decorators themselves must live on the action functions, not on wrappers around them.

## Risks / Trade-offs

- **Shell-string commands are slightly less type-safe than the current Python `subprocess.run([...])` list-argument calls** → mitigate by using `shlex.split` on the literal command string before passing to `subprocess.run`, keeping the same execution safety (no shell=True) while accepting a single string in the Gherkin text.
- **Placeholder substitution (`{tmp_dir}`, `{repo_root}`) in command strings adds a small templating layer** → keep it to two well-documented placeholders resolved by the `When` step, not a general templating engine.
- **A few scenarios still need small dedicated `Then` steps (YAML validity, file-content checks beyond substring)** → explicitly scoped and documented above rather than silently smuggled back in as "one function per scenario."
