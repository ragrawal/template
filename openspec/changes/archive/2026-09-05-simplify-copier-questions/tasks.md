## 1. Update the Copier answer schema

- [x] 1.1 In `templates/python-project/copier.yml`, remove the `project_name`, `description`, `author_name`, `author_email`, `license`, and `coverage_threshold` question blocks, leaving only `package_name` and `python_version`; verify by running `copier copy templates/python-project <tmp-dir> --data package_name=demo --defaults --trust` non-interactively and confirming Copier prompts for/accepts no other keys.
- [x] 1.2 SKIPPED per user decision: this template has no git tags, so Copier's `_migrations` never fires (it requires PEP 440 version tags on both sides of the update) - any entry added now would be inert. No existing users of the template exist yet, so `_migrations: []` is left untouched.

## 2. Update rendered templates

- [x] 2.1 In `templates/python-project/pyproject.toml.jinja`, drop the `description` field, the `[project.license]` conditional block, and the `authors` field entirely (an empty-name/no-email `authors` entry fails hatchling's build validation - discovered via `uv sync`, see design.md); verify the generated `pyproject.toml` has no `description`, `authors`, or `[project.license]` and that `uv sync` succeeds against it.
- [x] 2.2 In `templates/python-project/README.md.jinja`, change the heading to `# {{ package_name }}`, remove the description line, and remove the "## License" section; verify the generated `README.md`'s first line is `# demo` when `package_name=demo`.
- [x] 2.3 Delete `templates/python-project/LICENSE.jinja`; verify no `LICENSE` file appears in a freshly generated project.
- [x] 2.4 In `templates/python-project/AGENTS.md.jinja`, replace the `{{ project_name }}{% if description %} — {{ description }}{% endif %}` line with `{{ package_name }}`, and its separate `{{ coverage_threshold }}` reference with `80`; verify the generated `AGENTS.md` contains the package name and no leftover `{{ project_name }}`/`{{ description }}`/`{{ coverage_threshold }}` references.
- [x] 2.5 In `templates/python-project/src/{{ package_name }}/__init__.py.jinja`, replace `"""{{ description or (project_name + ".") }}"""` with a docstring based on `package_name` (e.g. `"""{{ package_name }}."""`); verify the generated `src/<package_name>/__init__.py` renders without a Jinja error.
- [x] 2.6 Hardcode the coverage threshold to `80` in place of every `{{ coverage_threshold }}` reference: `.coveragerc.jinja`, `AGENTS.md.jinja`, and `.claude/skills/run-quality-checks/SKILL.md.jinja`; verify `uv run poe check --full` in a generated project enforces an 80% threshold.

## 3. Update this repo's regression suite

- [x] 3.1 In `tests/bdd/python_project_test/python_project_test.feature`, remove `--data 'project_name=...'`, `--data 'author_name=...'`, `--data author_email=...`, `--data 'description=...'`, `--data license=...`, and `--data coverage_threshold=...` from every scenario's `copier copy` command; verify `uv run pytest tests/bdd/python_project_test` passes.
- [x] 3.2 Update the "Missing a required field fails generation" scenario to omit `-d package_name=...` (instead of `-d project_name`/`-d author_name`) and assert the output names `package_name`; verify the scenario passes.
- [x] 3.3 Remove the "Out-of-range coverage_threshold fails validation" scenario entirely, since `coverage_threshold` is no longer a Copier answer; verify the feature file has no remaining reference to `coverage_threshold`.
- [x] 3.4 Add/update assertions confirming the new fixed output: no `LICENSE` file is generated, `pyproject.toml` has no `description` or `authors` key, and `README.md`'s heading matches `package_name`; verify these assertions pass using the existing generic file/content step definitions in `tests/bdd/actions/` (added two new generic steps: "the following files do not exist" and "the file ... does not contain").

## 4. Full verification

- [x] 4.1 Run `uv run pytest` in this repository (this repo's actual CI check per `.github/workflows/template-regression.yml`; this repo itself has no `poe check` task/ruff/pyright - those only apply to generated downstream projects) and confirm it passes: 10 passed.
