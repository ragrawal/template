## 1. Move template content under `{{ package_name }}/`

- [x] 1.1 Create `templates/python-project/{{ package_name }}/` and move every existing top-level template file/directory into it — `pyproject.toml.jinja`, `README.md.jinja`, `AGENTS.md.jinja`, `.gitignore.jinja`, `.coveragerc.jinja`, `pytest.ini.jinja`, `ruff.toml.jinja`, `pyrightconfig.json.jinja`, `poe_tasks.toml.jinja`, `.github/`, `.claude/`, `src/{{ package_name }}/`, `tests/` — leaving only `copier.yml` directly under `templates/python-project/`. Verify with `find templates/python-project -maxdepth 1` showing just `copier.yml` and `{{ package_name }}`.
- [x] 1.2 Verify no file under `templates/python-project/{{ package_name }}/` (e.g. `pyproject.toml.jinja`'s `packages = ["src/{{ package_name }}"]`, `poe_tasks.toml.jinja`'s include path) references a path that assumed the old, shallower nesting; all such paths are already relative to the project root and require no edits since the whole subtree moved together — confirm by grepping for `"src/` and `include =` and checking they're still relative, single-level-correct paths.

## 2. Update this repository's regression suite

- [x] 2.1 Update every scenario in `tests/bdd/python_project_test/python_project_test.feature` so file-existence assertions and `uv sync` / `uv run poe ...` working directories point at `{tmp_dir}/project/demo/...` (or `{tmp_dir}/project/custom_widgets/...` where that answer is used) instead of `{tmp_dir}/project/...`, matching the new `<package_name>/` nesting. Verify by running `uv run pytest` and confirming all scenarios pass.
- [x] 2.2 Confirm the "A broken template produces a clear failure" scenario: `given_broken_template_source` in `tests/bdd/actions/files.py` copies the whole `templates/python-project` tree wholesale via `shutil.copytree` (no edit needed there), but it also directly edits `ruff.toml.jinja` inside that copy assuming it sits at the template root — that path needed updating to `{{ package_name }}/ruff.toml.jinja` to match the new nesting. Verified via the `uv run pytest` run below.
- [x] 2.3 Verify no stray `__pycache__` or other artifacts appear anywhere under the new `<package_name>/` nesting by running the full suite and confirming the existing "no `__pycache__` directories exist" assertions still pass, and that `git status --porcelain` in this repository is unchanged after the run.

## 3. Update repository documentation

- [x] 3.1 Update `README.md`'s "Using this template" section to state that `copier copy templates/python-project path/to/new-project` creates the project at `path/to/new-project/<package_name>/`, not directly in `path/to/new-project/`.
- [x] 3.2 Update `openspec/project.md`'s architecture notes to mention that generated output is nested under a `{{ package_name }}/` folder inside `templates/python-project/`, alongside the existing note about no `_subdirectory` being set.

## 4. Full verification

- [x] 4.1 Run `uv run pytest` from the repository root and confirm the entire regression suite passes against the restructured template.
- [x] 4.2 Manually run `uv tool run copier copy templates/python-project /tmp/manual-check --data package_name=demo --defaults --trust` and confirm the result is `/tmp/manual-check/demo/pyproject.toml` (not `/tmp/manual-check/pyproject.toml`), then remove the scratch directory.
