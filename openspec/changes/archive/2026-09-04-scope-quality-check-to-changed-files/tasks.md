## 1. Dispatch script

- [x] 1.1 Add `templates/python-project/scripts/quality_check.py.jinja` (or equivalent) that: detects `CI` env var / `--full` flag, computes changed files via `git diff --name-only` against the merge-base with the default branch (falling back to `HEAD` if no merge-base found), and dispatches to `ruff format --check`, `ruff check`, `pyright`, and `pytest`/`pytest --testmon` with the right file scope. Verify by running it directly against a sample diff and confirming it prints which mode (scoped/full) it chose.
- [x] 1.2 Wire `poe_tasks.toml.jinja`'s `check` task to call the new script instead of the `format-check`/`typecheck`/`test` sequence; leave `format`, `lint`, `typecheck`, `test` sub-tasks unchanged (still full-repo, independently invocable). Verify with `uv run poe check --help`/`uv run poe check` showing the new dispatch behavior.

## 2. Test-impact analysis

- [x] 2.1 Add `pytest-testmon` to the dev dependency group in `templates/python-project/pyproject.toml.jinja`. Verify `uv sync --locked` succeeds in a freshly generated project.
- [x] 2.2 Add `.testmondata` to `templates/python-project/.gitignore.jinja`. Verify `git status` is clean after a local scoped run in a generated project.
- [x] 2.3 Implement the fallback in the dispatch script: no `.testmondata` present -> run the full test suite once (building the cache) instead of erroring. Verify by deleting `.testmondata` and confirming a full test run occurs and the cache is recreated.

## 3. Template regression coverage

- [x] 3.1 Add or extend a `tests/bdd/` scenario in this repository asserting that a generated project's `uv run poe check` still passes end-to-end (full path, since the regression job runs with `CI` set). Verify by running `uv run pytest` in this repository.
- [x] 3.2 Add a scenario (or extend an existing generic step) exercising the local/scoped path directly against a generated project (e.g. invoke the dispatch script with `CI` unset and a small diff) and assert it only touches the expected file subset. Verify by running `uv run pytest` in this repository.

## 4. Documentation

- [x] 4.1 Update `templates/python-project/README.md.jinja` and/or `AGENTS.md.jinja` to document the default scoped `check` behavior, the `--full` override, and the `.testmondata` cache. Verify by reviewing the rendered docs in a freshly generated project.
- [x] 4.2 Update this repository's own `README.md` "Developing template" section if the regression-suite invocation changes. Verify by re-reading the rendered section for accuracy. (No change needed: the regression-suite invocation, `uv run pytest`, is unchanged, and this file doesn't otherwise reference `poe check`.)

## 5. Full verification

- [x] 5.1 Generate a project via `uv tool run copier copy templates/python-project <tmp-dir> --defaults --trust`, make a small source-only edit, and confirm `uv run poe check` (no `CI` set) only reports on the changed file and reruns only affected tests. Verify manually.
- [x] 5.2 In the same generated project, set `CI=true uv run poe check` (or `uv run poe check --full`) and confirm the full format/lint/typecheck/test suite runs regardless of the small diff. Verify manually.
- [x] 5.3 Run `openspec validate scope-quality-check-to-changed-files --strict` and confirm it passes before archiving.
