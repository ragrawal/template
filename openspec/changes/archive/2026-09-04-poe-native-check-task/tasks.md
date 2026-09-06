## 1. Poe task definitions

- [x] 1.1 Rewrite the `[tasks.test]` entry in `templates/python-project/poe_tasks.toml.jinja` as a `shell` task with a `--full` boolean arg that runs `pytest --testmon -o addopts=` by default and plain `pytest` when `--full` is passed. Verify with `uv run poe test` and `uv run poe test --full` in a locally generated project, confirming the former uses testmon output and the latter reports full coverage.
- [x] 1.2 Rewrite the `[tasks.check]` entry as a `sequence` task with its own `--full` boolean arg, referencing `format-check`, `lint`, `typecheck`, and `test ${full:+--full}` in order. Verify with `uv run poe check --help` showing the `--full` flag, and `uv run poe check` / `uv run poe check --full` both running all four steps in order.
- [x] 1.3 Delete `templates/python-project/scripts/quality_check.py` and remove the now-empty `scripts/` directory if nothing else lives there. Verify with `grep -r quality_check templates/python-project` returning no matches.

## 2. CI workflow

- [x] 2.1 Update `templates/python-project/.github/workflows/quality.yml.jinja` to run `uv run poe check --full` instead of `uv run poe check`. Verify by regenerating a project and confirming the workflow YAML contains `poe check --full`.

## 3. Documentation

- [x] 3.1 Update `templates/python-project/README.md.jinja` to describe the new default (`check`/`test` testmon-scoped by default) and `--full` (whole suite, coverage enforced) behavior, removing references to diff-scoping and the `CI` environment variable. Verify by reviewing the rendered README in a freshly generated project.
- [x] 3.2 Update `templates/python-project/AGENTS.md.jinja` with the same corrected description. Verify by reviewing the rendered file in a freshly generated project.
- [x] 3.3 Update `templates/python-project/.claude/skills/run-quality-checks/SKILL.md.jinja` with the same corrected description, including that `uv run poe check --full` (not just running in CI) is what gives the coverage-enforced full-project guarantee. Verify by reviewing the rendered file in a freshly generated project.

## 4. Template regression coverage

- [x] 4.1 In `tests/bdd/python_project_test/python_project_test.feature`, replace the "CI environment variable forces the full check regardless of diff size" scenario with one asserting `uv run poe check --full` runs the complete suite with coverage enforced (e.g. assert on coverage output), dropping the `CI set`/`"Running full quality check"` assertions. Verify by running `uv run pytest` in this repository.
- [x] 4.2 Replace the "Local check without CI scopes to files changed since the last commit" scenario with one asserting `uv run poe check` (no `--full`) runs test via testmon while lint/format/typecheck still run against the whole project, dropping the `CI unset`/`"Running scoped quality check"` assertions. Verify by running `uv run pytest` in this repository.
- [x] 4.3 Extend the "Each Poe the Poet task follows its exit-code contract" scenario (or add a new one) to also invoke `uv run poe test --full` and `uv run poe check --full`, confirming both exit `0`. Verify by running `uv run pytest` in this repository.

## 5. Full verification

- [x] 5.1 Generate a project via `uv tool run copier copy templates/python-project <tmp-dir> --defaults --trust`, run `uv sync`, then `uv run poe check` and confirm format/lint/typecheck run against the whole project and test uses testmon. Verify manually.
- [x] 5.2 In the same generated project, run `uv run poe check --full` and confirm all four steps run against the entire project with the test step reporting enforced coverage. Verify manually.
- [x] 5.3 Run `openspec validate poe-native-check-task --strict` and confirm it passes before archiving.
