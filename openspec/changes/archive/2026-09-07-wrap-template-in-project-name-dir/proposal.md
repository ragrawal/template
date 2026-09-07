## Why

Today `copier copy templates/python-project <dest>` renders the project directly into `<dest>` (e.g. `<dest>/pyproject.toml`, `<dest>/src/<package_name>`), so whether the generated project ends up in its own named folder depends entirely on what destination path the caller happens to pass to the Copier CLI — the template itself never creates that folder. The template should own this: it should always render its output under a folder named after the package, so a single `copier copy templates/python-project <dest>` reliably produces `<dest>/<package_name>/src/<package_name>` regardless of what destination path is passed.

## What Changes

- **BREAKING**: Move every file currently rendered directly under `templates/python-project/` (`pyproject.toml.jinja`, `README.md.jinja`, `AGENTS.md.jinja`, `.gitignore.jinja`, `.coveragerc.jinja`, `pytest.ini.jinja`, `ruff.toml.jinja`, `pyrightconfig.json.jinja`, `poe_tasks.toml.jinja`, `.github/`, `.claude/`, `src/`, `tests/`) into a new `templates/python-project/{{ package_name }}/` directory. `copier.yml` stays at `templates/python-project/copier.yml` (unaffected, since Copier's default excludes already skip it and there is no `_subdirectory` setting).
- No new answer is introduced — the wrapping folder name reuses the existing `package_name` answer, keeping the schema at two prompts (`package_name`, `python_version`), consistent with the `simplify-copier-questions` change.
- Update this repository's own regression suite (`tests/bdd/python_project_test/`) so every asserted file path and every `uv sync` / `uv run poe ...` working directory accounts for the new `<package_name>/` nesting under the destination the test passes to `copier copy`.

## Capabilities

### New Capabilities

(none)

### Modified Capabilities

- `template-generation`: generated output now lands under a `<package_name>/` folder inside the destination passed to `copier copy`, rather than directly in that destination.

## Impact

- `templates/python-project/`: every file except `copier.yml` moves one directory level deeper, under `templates/python-project/{{ package_name }}/`.
- `tests/bdd/python_project_test/python_project_test.feature` and any step definitions that hardcode `{tmp_dir}/project/...` paths or `in "{tmp_dir}/project"` working directories.
- Downstream consumers: running `copier copy templates/python-project <dest>` now creates `<dest>/<package_name>/...` instead of `<dest>/...`; anyone already working around this by passing a destination that matches their intended package name will get an extra, redundant nesting level and should instead pass a parent directory as `<dest>`.
- No change to `copier.yml`'s answer schema, so no `_migrations` entry is needed — `copier update` on already-generated projects is a template-source-location change, not an answer-schema change, and is out of scope here (existing generated projects were not created under the new nesting and are unaffected until they are regenerated from scratch).
