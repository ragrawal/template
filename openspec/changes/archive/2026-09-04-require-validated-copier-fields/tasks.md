## 1. Harden `copier.yml`

- [x] 1.1 Add `undefined: StrictUndefined` under `_envops` in `copier.yml` and verify `uv tool run copier copy . /tmp/x --defaults --trust` still succeeds with all fields answered via `-d`
- [x] 1.2 Remove the `default:` key from `package_name` in `copier.yml` and verify running with `--defaults` and no `-d package_name=...` fails with a "Question is required" error naming `package_name`
- [x] 1.3 Remove the `default:` key from `coverage_threshold` in `copier.yml` and verify running with `--defaults` and no `-d coverage_threshold=...` fails with a "Question is required" error naming `coverage_threshold`
- [x] 1.4 Confirm `author_email`, `description`, `python_version`, and `license` are unchanged and still generate successfully when omitted under `--defaults`

## 2. Update this repo's own regression scenarios for the new required fields

- [x] 2.1 Update the "Generate a project with default answers" and "Each Poe the Poet task follows its exit-code contract" and "The generated project ships a valid PR-triggered quality workflow" and "The generated project ships AI agent guidance and a quality-check skill" scenarios (plus "A broken template produces a clear failure", which hit the same now-required-field gap and wasn't listed here) in `tests/bdd/python_project_test/python_project_test.feature` to add `--data package_name=... --data coverage_threshold=...` (now required) and verify `uv run pytest -v` still passes all of them

## 3. Add BDD coverage for the two new failure modes

- [x] 3.1 Add a "Missing a required field fails generation" scenario to `tests/bdd/python_project_test/python_project_test.feature` using the existing generic steps (`Given a temporary directory`, `When the user runs "..."`, `Then the command exits with a non-zero code`, `Then the output contains "..."`) and verify it passes with no new step functions added
- [x] 3.2 Add an "Out-of-range coverage_threshold fails validation" scenario to the same feature file, running with `--data coverage_threshold=150` (or `-5`), and verify it passes using only existing generic steps
- [x] 3.3 Run `uv run pytest -v` from the repo root and verify all scenarios pass, including the two new ones

## 4. Soften the `write-bdd-tests` skill's step-placement guidance

- [x] 4.1 Update `.claude/skills/write-bdd-tests/SKILL.md` to replace the "contains nothing but... Do not add step functions there" / "never as a thin wrapper" wording with a stated preference for generic steps in `tests/bdd/actions/`, plus an explicit exception for steps genuinely specific to one feature and not reusable elsewhere
- [x] 4.2 Apply the equivalent wording change to `templates/python-project/.claude/skills/write-bdd-tests/SKILL.md.jinja` and verify the two files describe the same guidance (diff the relevant section)

## 5. Validate

- [x] 5.1 Run `openspec validate require-validated-copier-fields --strict` and confirm it passes
- [x] 5.2 Run `uv run pytest` and `uv tool run ruff check --select F401,F841 tests/` from the repo root and confirm both are clean
