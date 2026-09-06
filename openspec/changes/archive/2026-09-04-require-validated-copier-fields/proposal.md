## Why

Running Copier against the wrong entry point (e.g. `copier copy ~/template/template <dst>`, pointing at the `template/` subdirectory instead of the repo root that holds `copier.yml`) bypasses every question, validator, and `_envops` setting in `copier.yml`. Jinja's default `Undefined` then silently stringifies missing variables to `""` instead of erroring, so `project_name`, `author_name`, and friends render blank with no warning. Separately, two answer fields (`package_name`, `coverage_threshold`) currently ship a `default:`, which lets Copier silently accept a generated or stale value even when the caller never consciously supplied one. Neither gap is caught by the current regression suite, and the `write-bdd-tests` skill's step-placement rule is stricter than the team actually wants to follow.

## What Changes

- Add `_envops: undefined: StrictUndefined` to `copier.yml` so any template variable left undefined during rendering raises a hard `UndefinedError` instead of silently rendering as an empty string. This is what actually fixes the reported "didn't ask for any fields" failure mode (which was caused by bypassing `copier.yml` entirely, not by any field being individually optional).
- **BREAKING**: Remove the `default:` key from `package_name` and `coverage_threshold` in `copier.yml`, making every field that carries a `validator:` unconditionally required except `author_email` (its validator only fires when a value is supplied, so it stays optional). `project_name` and `author_name` are already required today and need no change. `description`, `python_version`, and `license` have no validator and stay optional/defaulted. Existing automation that runs `copier copy ... --defaults` without explicitly answering `package_name` or `coverage_threshold` will now fail fast with "Question is required" instead of silently using the previous computed/default value.
- Add a new BDD scenario asserting that omitting a required field (`project_name`, `author_name`, `package_name`, or `coverage_threshold`) when generating via `--defaults` causes Copier to exit non-zero with a clear error, rather than silently succeeding.
- Add a new BDD scenario asserting that an out-of-range `coverage_threshold` (e.g. `-5` or `150`) is rejected by its existing validator.
- Update the `write-bdd-tests` skill (both this repo's `.claude/skills/write-bdd-tests/SKILL.md` and the template's `template/.claude/skills/write-bdd-tests/SKILL.md.jinja`) to soften the step-placement rule: prefer generic, reusable step functions in the shared `tests/bdd/actions/` modules, but a step that is genuinely specific to one feature and not reusable elsewhere may live directly in that feature's own file. State this as a guideline, not a strict rule.

## Capabilities

### New Capabilities

(none)

### Modified Capabilities

- `template-generation`: `copier.yml`'s answer schema changes (fields become unconditionally required except `author_email`; `_envops` gains `StrictUndefined`) are a spec-level, externally observable behavior change to how the template is generated.
- `template-regression-testing`: new scenarios cover the missing-required-field failure and the out-of-range `coverage_threshold` failure.
- `ai-agent-guidance`: the bundled `write-bdd-tests` skill's documented step-placement guidance changes from a strict rule to a general preference.

## Impact

- `copier.yml` (root): `_envops`, `package_name`, `coverage_threshold`.
- `tests/bdd/template_generation/template_generation.feature` and `tests/bdd/actions/shell.py` (or a new actions module) in this repo: new scenarios/steps for missing-field and out-of-range-threshold failures.
- `.claude/skills/write-bdd-tests/SKILL.md` and `template/.claude/skills/write-bdd-tests/SKILL.md.jinja`: wording change only.
- Downstream consumers of this template who script `copier copy ... --defaults` without explicitly answering `package_name` or `coverage_threshold` will need to start passing `-d package_name=... -d coverage_threshold=...` (or drop `--defaults` and answer interactively).
