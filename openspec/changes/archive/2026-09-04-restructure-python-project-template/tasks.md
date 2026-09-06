## 1. Move the template source

- [x] 1.1 Create `templates/python-project/` and move `copier.yml` and `template/` into it (plain `mv`, since this project directory is untracked in the enclosing home-directory git repo) and verify `templates/python-project/copier.yml` and `templates/python-project/template/` exist with no leftover `copier.yml`/`template/` at the repo root
- [x] 1.2 Verify `templates/python-project/copier.yml`'s `_subdirectory: template` still resolves correctly by running `uv tool run copier copy templates/python-project /tmp/rpt-check --trust --defaults -d project_name=Check -d author_name=Author -d package_name=check -d coverage_threshold=80` and confirming a project is generated

## 2. Rename and update this repo's own regression feature

- [x] 2.1 Rename `tests/bdd/template_generation/` to `tests/bdd/python_project_test/`, `template_generation.feature` to `python_project_test.feature`, and `test_template_generation.py` to `test_python_project_test.py`, updating the `scenarios(...)` call to `scenarios("python_project_test.feature")`
- [x] 2.2 Update every `uv tool run copier copy {repo_root} ...` command in `python_project_test.feature` to `uv tool run copier copy {repo_root}/templates/python-project ...` and verify with `uv run pytest --collect-only -q`
- [x] 2.3 Update `tests/bdd/actions/files.py`'s `given_broken_template_source` to copy `repo_root / "templates" / "python-project" / "copier.yml"` and `repo_root / "templates" / "python-project" / "template"` and verify the "A broken template produces a clear failure" scenario still passes
- [x] 2.4 Run `uv run pytest -v` from the repo root and verify all scenarios in `tests/bdd/python_project_test/` pass

## 3. Update documentation and skill references

- [x] 3.1 Update `README.md`'s usage example to `uv tool run copier copy <this-repo-url-or-path>/templates/python-project path/to/new-project` and verify by reading the rendered section
- [x] 3.2 Update `openspec/project.md`'s Architecture Patterns section to reference `templates/python-project/copier.yml` + `templates/python-project/template/`, and correct its stale Testing Strategy reference from `tests/features/*.feature` + `tests/steps/` to `tests/bdd/*.feature` + `tests/bdd/actions/`
- [x] 3.3 Update `.claude/skills/write-bdd-tests/SKILL.md`'s example binding-file path from `tests/bdd/template_generation/test_template_generation.py` to `tests/bdd/python_project_test/test_python_project_test.py`

## 4. Validate

- [x] 4.1 Run `openspec validate restructure-python-project-template --strict` and confirm it passes
- [x] 4.2 Run `git status --porcelain` before and after a full `uv run pytest` run from the repo root and confirm the working tree is unchanged (per the `template-regression-testing` no-stray-artifacts requirement)
- [x] 4.3 Grep the repo for any remaining reference to a root-level `copier.yml`/`template/` path outside `templates/python-project/` and `openspec/changes/` (e.g. `grep -rn "copier copy \${repo_root}\"\|_subdirectory: template" --include="*.md" --include="*.py" --include="*.feature" .`) and update or confirm each remaining hit is intentional (e.g. inside archived change history, which is left as historical record)
