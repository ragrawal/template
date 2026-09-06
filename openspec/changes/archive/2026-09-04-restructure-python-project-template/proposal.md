## Why

This repository will eventually host more than one Copier template (a Python project template, an ML project template, etc.), but today `copier.yml` and `template/` live at the repo root as if this were a single-template repository. Before adding any new template, the existing Python template needs to move into a named slot so future templates can sit alongside it without a redesign.

## What Changes

- **BREAKING**: Move `copier.yml` and `template/` from the repo root into `templates/python-project/copier.yml` and `templates/python-project/template/`. Downstream consumers must change `uv tool run copier copy <this-repo> <dst>` to `uv tool run copier copy <this-repo>/templates/python-project <dst>`.
- Rename this repository's own regression-test feature from `tests/bdd/template_generation/` (`template_generation.feature` / `test_template_generation.py`) to `tests/bdd/python_project_test/` (`python_project_test.feature` / `test_python_project_test.py`), and update its `copier copy` command strings to point at `{repo_root}/templates/python-project`.
- Update `tests/bdd/actions/files.py`'s broken-template setup step to copy from `templates/python-project/copier.yml` and `templates/python-project/template/`.
- Update `README.md` and `openspec/project.md` usage/architecture text to reference the new `templates/python-project/` path (also correcting `openspec/project.md`'s stale reference to `tests/features/`/`tests/steps/`, which predates the existing `tests/bdd/` layout).
- Update the `write-bdd-tests` skill's example binding-file path to match the renamed feature.

## Capabilities

### New Capabilities

(none)

### Modified Capabilities

- `template-generation`: the Copier template source's location changes from the repo root (`copier.yml` + `template/`) to `templates/python-project/` (`templates/python-project/copier.yml` + `templates/python-project/template/`); the "only the template subtree is rendered" boundary is now scoped to that directory.

## Impact

- Repo root: `copier.yml`, `template/` move to `templates/python-project/`.
- `tests/bdd/template_generation/` renamed to `tests/bdd/python_project_test/`; `tests/bdd/actions/files.py` updated.
- `README.md`, `openspec/project.md`, `.claude/skills/write-bdd-tests/SKILL.md` updated for the new path.
- No change to `template/`'s own contents, to `copier.yml`'s answer schema, or to any generated-project behavior.
- Downstream consumers pointing at this repo's root as a Copier source must update to `templates/python-project/`.
- The sibling in-flight change `require-validated-copier-fields` (not yet applied) targets `copier.yml` at the repo root; once this change is archived, that change's tasks and file references will need updating to the new `templates/python-project/copier.yml` path before it is applied.
