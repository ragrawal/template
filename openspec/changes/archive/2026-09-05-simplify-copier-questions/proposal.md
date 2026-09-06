## Why

The template currently prompts for eight answers (`project_name`, `package_name`, `description`, `author_name`, `author_email`, `python_version`, `license`, `coverage_threshold`) before it will generate a project. Most of these have an obvious, safe default or duplicate information already given by another answer, so they add friction without adding real choice. Reducing the prompt set to the two answers that actually vary per project (`package_name`, `python_version`) makes bootstrapping a new project faster.

## What Changes

- **BREAKING**: Remove the `project_name` question. `project_name` is no longer a prompted answer; every place that rendered it (`README.md.jinja` heading, `AGENTS.md.jinja`, skill docs) now renders `package_name` literally instead.
- **BREAKING**: Remove the `description` question. `pyproject.toml`'s `description` field is no longer rendered (dropped from the `[project]` table rather than emitted as an empty string).
- **BREAKING**: Remove the `author_name` and `author_email` questions. `pyproject.toml`'s `authors` field is dropped entirely (an entry with an empty `name` and no `email` fails hatchling's build validation, and `authors` is optional under PEP 621).
- **BREAKING**: Remove the `license` question. No `LICENSE` file is generated and `pyproject.toml` no longer emits a `[project.license]` table (equivalent to today's `license: None` choice). `README.md.jinja`'s "## License" section is removed.
- **BREAKING**: Remove the `coverage_threshold` question. `.coveragerc`'s enforced threshold is now a fixed `80`, no longer a Copier answer.
- Remaining questions: `package_name` and `python_version` only.
- Update `_migrations` in `copier.yml` so `copier update` on a previously generated project maps the old answers onto the new, smaller schema without erroring (dropped keys are simply discarded; `project_name` is not carried forward since it's no longer stored).

## Capabilities

### New Capabilities

(none)

### Modified Capabilities

- `template-generation`: the Copier answer schema shrinks from eight prompted fields to two (`package_name`, `python_version`); `project_name`, `description`, `author_name`, `author_email`, `license`, and `coverage_threshold` are no longer prompted, several are removed from rendered output entirely (`LICENSE` file, `[project.license]`, `description` field), and others take a fixed value (`authors` name empty, coverage threshold fixed at 80, `project_name` equals `package_name`).

### Modified Capabilities (test coverage)

- `template-regression-testing`: existing scenarios and fixtures that answer or assert on `project_name`, `description`, `author_name`, `author_email`, `license`, or `coverage_threshold` need updating to match the reduced schema and new fixed outputs.

## Impact

- `templates/python-project/copier.yml`: removes six question definitions, updates `_migrations`.
- `templates/python-project/template/pyproject.toml.jinja`: drops `description`, `authors`, and `[project.license]` entirely.
- `templates/python-project/template/README.md.jinja`: heading uses `package_name`; drops the description line and the "## License" section.
- `templates/python-project/template/LICENSE.jinja`: deleted; no longer rendered.
- `templates/python-project/template/AGENTS.md.jinja`, `.claude/skills/run-quality-checks/SKILL.md.jinja`, `.claude/skills/write-bdd-tests/SKILL.md.jinja`, `src/{{ package_name }}/__init__.py.jinja`: any `project_name`/`description` reference switches to `package_name` or is dropped.
- `.coveragerc` (generated): threshold hardcoded to `80`.
- Downstream repos previously generated with this template: running `copier update` drops the now-unused answers per the new `_migrations` entry; their existing `LICENSE`, description, and author metadata are untouched (Copier does not retroactively delete files it once generated).
- This repo's own `tests/bdd/` fixtures/features covering template generation.
