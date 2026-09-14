## Why

Running `templates/ml` against a destination path of `.` (e.g. `cd house_price && copier copy .../templates/ml . --trust`) silently drops every file under `src/<package_name>/` (`estimator.py`, `schema.py`, `tasks/`) with no error: `package_name` defaults to `_copier_conf.dst_path.name`, which is an empty string when the destination argument is `.`, and Copier treats an empty rendered path segment as "skip this file." Separately, when the destination isn't a valid `templates/python-project` output, the prerequisite check (task 1) still leaves every rendered file behind on failure, because Copier always renders files before running `_tasks`. Finally, all of the ML overlay's own test files land flat under `tests/` instead of mirroring the `src/<package_name>/` and `webapp/` layout they test, making it unclear which test covers which module as the overlay grows.

## What Changes

- Detect the empty-`package_name` case (the `dst_path == "."` case) as a post-render `_tasks` check in `templates/ml/copier.yml` that fails generation with a clear, actionable message instead of silently skipping files, and deletes the files this run added before exiting non-zero. (A `package_name` question `validator:` was tried first but never fires here: the question has `when: false`, required to keep the documented flagless, non-interactive invocation working.)
- Change the prerequisite check (currently `_tasks` entry 1: `test -f .answers/.python_project.yml || ...`) so that on failure it deletes the files/directories this template overlay just wrote, restoring the destination to its pre-run state, before exiting non-zero. This check continues to run before the `uv add` tasks.
- Reorganize `templates/ml/tests/` so each test file's location mirrors the source module it covers: `test_estimator.py` and `test_schema.py` move under `tests/<package_name>/`, `test_train_model.py` moves under `tests/<package_name>/tasks/`, and `test_app.py` moves under `tests/webapp/`.
- Update the existing `tests/bdd/ml_overlay_test` regression suite and `templates/ml/docs/ML_README.md.jinja` (if it documents test locations) to match the new layout and to cover the empty-`package_name` and failed-prerequisite-cleanup scenarios.

## Capabilities

### New Capabilities
(none)

### Modified Capabilities
- `ml`: `package_name` derivation must fail clearly instead of silently omitting files when it resolves to an empty string; a failed prerequisite check must leave no partially-generated files in the destination; generated test files must be organized under `tests/<package_name>/` and `tests/webapp/` to mirror the source layout instead of a flat `tests/` directory.

## Impact

- `templates/ml/copier.yml`: rework `_tasks` entry 1 into a check-and-cleanup step, and add a second `_tasks` check-and-cleanup step detecting an empty-derived `package_name`.
- `templates/ml/tests/*.jinja` → moved to `templates/ml/tests/{{ package_name }}/`, `templates/ml/tests/{{ package_name }}/tasks/`, and `templates/ml/tests/webapp/`.
- `tests/bdd/ml_overlay_test/ml_overlay_test.feature` and its step bindings: new scenarios for the empty-destination-name failure and the cleanup-on-failed-prerequisite-check behavior; updated file-existence assertions for the new test paths.
- `templates/ml/docs/ML_README.md.jinja`: update any references to test file locations.
- No changes to `templates/python-project` or its specs.
