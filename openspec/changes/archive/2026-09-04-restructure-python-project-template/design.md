## Context

See proposal.md - Why. Current state: `copier.yml` and `template/` live at the repo root; `copier.yml`'s `_subdirectory: template` is a path relative to wherever `copier.yml` itself lives, so it does not need to change when both move together. This repo's own `tests/bdd/template_generation/template_generation.feature` and `tests/bdd/actions/files.py` (`given_broken_template_source`) are the only places that hard-code the source layout (`repo_root` + `copier.yml` / `template`). `README.md` and `openspec/project.md` document the current root-level usage and architecture.

## Goals / Non-Goals

**Goals:**
- Move the existing Python template into `templates/python-project/` with zero behavior change to what a generated project looks like.
- Update every reference to the old root-level `copier.yml`/`template/` path across this repo's tests, docs, and skill examples so nothing is left pointing at a path that no longer exists.
- Rename the regression-test feature to `python_project_test` to reflect that it tests one specific template, not "the template" in general.

**Non-Goals:**
- Adding a second template (e.g. an ML project template) — confirmed out of scope; this change only relocates the existing one.
- Any shared/common utilities across future templates — confirmed out of scope.
- Renaming OpenSpec capability paths (e.g. `template-generation` → `python-project/template-generation`) to nest under a per-template namespace. The sibling in-flight change `require-validated-copier-fields` already has delta specs and tasks against the unqualified `template-generation`/`template-regression-testing`/`ai-agent-guidance` paths; renaming capability paths here would force that change to be rewritten before it can be applied. Deferred to a future change once capability-level organization for multiple templates is actually needed (i.e., when a second template is added).
- Changing `copier.yml`'s answer schema, `_envops`, or any templated file content.

## Decisions

**New path is `templates/python-project/`, not `templates/python/` or a root dispatcher.** `python-project` names what gets generated (an installable Python project), matching this repo's own existing terminology (`template-generation`'s requirement text already says "Python project scaffold"). A root-level dispatcher `copier.yml` that forwards to sub-templates was considered and rejected: Copier has no built-in "pick a sub-template" primitive, it would require bespoke `_tasks`/prompt logic to reimplement what "point Copier at a different subdirectory" already does natively, and it would add indirection with no present benefit since there is only one template today.

**Feature/directory renamed to `python_project_test`, per explicit instruction.** `tests/bdd/template_generation/` becomes `tests/bdd/python_project_test/`, with `python_project_test.feature` and `test_python_project_test.py`, following the existing convention (`tests/bdd/<feature>/<feature>.feature` + `test_<feature>.py`). The name repeats "test" in the binding filename (`test_python_project_test.py`) but this is what was asked for and keeps the file naming pattern intact.

**`copier.yml`'s own content and `_subdirectory: template` do not change.** Only its filesystem location changes; `_subdirectory` is already relative to `copier.yml`'s own directory, so the two moving together requires no internal edit.

**Command strings gain a literal `/templates/python-project` path segment.** Every `uv tool run copier copy {repo_root} ...` in the feature file becomes `uv tool run copier copy {repo_root}/templates/python-project ...`, keeping the existing `{repo_root}`/`{tmp_dir}` placeholder convention from `tests/bdd/actions/shell.py` rather than inventing a new placeholder.

**`openspec/project.md`'s stale `tests/features/`/`tests/steps/` reference is corrected while this doc is already being touched for the path move.** It predates the `tests/bdd/` restructuring done in the already-archived `adopt-generic-bdd-steps` change and was missed at the time; fixing it here is a same-file, same-section correction, not new scope.

## Risks / Trade-offs

- [Risk] Breaks any script or documentation outside this repo that points at the repo root as a Copier source. → Mitigation: this is the intended, documented **BREAKING** change (there is no known external consumer yet per the project's early stage), and `README.md` is updated to show the new command.
- [Risk] The sibling in-flight change `require-validated-copier-fields` (already fully planned, not yet applied) has tasks and delta specs written against the old root `copier.yml` path. → Mitigation: apply and archive this change first (as the user requested), then update `require-validated-copier-fields`'s tasks.md/design.md path references to `templates/python-project/copier.yml` before applying it. No spec-level rework is needed there since its delta specs describe answer-schema behavior, not file location.
