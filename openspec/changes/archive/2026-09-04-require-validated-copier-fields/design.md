## Context

See proposal.md - Why. Relevant current state: `copier.yml` (repo root) declares `_subdirectory: template` and has no `_envops.undefined` setting, so Jinja's default `Undefined` silently stringifies missing variables to `""`. `package_name` and `coverage_threshold` currently have a `default:` despite both having a `validator:` that assumes a value is present. `author_email`'s validator only fires when a value is supplied (`{% if author_email and ... %}`), so it is optional by design. This repo's own regression suite (`template-regression-testing`) already generates real projects via `copier copy` and has a generic, reusable step vocabulary in `tests/bdd/actions/` (`shell.py`, `files.py`) that the new scenarios reuse as-is.

## Goals / Non-Goals

**Goals:**
- Make Copier fail loudly, not silently, whenever a template variable ends up undefined at render time — this is the actual fix for the reported bug.
- Make every field whose validator unconditionally assumes a value present required, except `author_email`.
- Cover both failure modes (missing required field, out-of-range `coverage_threshold`) with regression scenarios using the existing generic step vocabulary — no new step functions needed.
- Soften the `write-bdd-tests` skill's step-placement rule from a strict "never" to a stated preference with a documented, narrow exception.

**Non-Goals:**
- Restructuring this repo to support multiple template types (Python, ML, etc.) — deferred to its own change per the user's explicit request.
- Adding a Copier migration — see Decisions below for why one isn't needed here.
- Changing `author_email`, `description`, `python_version`, or `license` — they stay optional/defaulted.

## Decisions

**Add `_envops.undefined: StrictUndefined` rather than only removing defaults.** Removing `package_name`/`coverage_threshold`'s defaults does not fix the reported bug: the user's failing command pointed Copier at `template/` directly, which has no `copier.yml` at all, so no question is ever prompted for *any* field regardless of whether it has a default. `StrictUndefined` is the actual fix — it makes Jinja raise on any variable that never got a value, independent of how it failed to get one (wrong entry point, an aborted prompt, a future template bug). Alternative considered: only removing defaults and calling it done — rejected because it would not have caught the user's actual failure and would give false confidence.

**Make `package_name` and `coverage_threshold` required (remove their `default:`).** Both have a `validator:` that unconditionally assumes a value already exists (`package_name | regex_search(...)`, `coverage_threshold < 0 or > 100`) — an empty/missing value at validation time would either fail confusingly or (for `coverage_threshold`, an `int` field) not apply at all. Making them required surfaces the same class of problem the user hit, one level earlier, as a clear "Question is required" error instead of a downstream validator failure or silent default. `author_email` is deliberately excluded per the user's explicit instruction, since its validator is conditional on a non-empty value and it has no correctness requirement to enforce.

**No `_migrations` entry needed.** The compatibility requirement in `template-generation` triggers when "changing a default in a way that changes generated output for existing answers." `copier update` re-uses each question's previously-recorded answer from `.copier-answers.yml` rather than re-prompting; a project that was already generated has concrete stored values for `package_name` and `coverage_threshold`, so removing the schema-level default does not change what `copier update` produces for it. The only affected case is a *new* generation that used to rely on the default and no longer can — that is the intended, documented **BREAKING** change in the proposal, not an update-compatibility concern.

**New regression scenarios reuse existing generic steps.** `Given a temporary directory` / `When the user runs "<command>"` / `Then the command exits with a non-zero code` / `Then the output contains "<text>"` (already in `tests/bdd/actions/shell.py`) are sufficient to express both new scenarios. No new step functions are needed, which also serves as a concrete example of the `template-regression-testing` requirement that new scenarios must be expressible with existing steps.

**Skill wording change is additive, not restructured.** Replace the "contains nothing but... Do not add step functions there" / "never as a thin wrapper" language with a stated default (generic steps in `tests/bdd/actions/`) plus a narrow, explicit exception (truly feature-specific, non-reusable steps may live in that feature's own file). Apply the same wording change to both `.claude/skills/write-bdd-tests/SKILL.md` (this repo) and `template/.claude/skills/write-bdd-tests/SKILL.md.jinja` (shipped to generated projects) so the two stay in sync, as they already are for every other convention they document.

## Risks / Trade-offs

- [Risk] Any existing script or CI job that runs `copier copy ... --defaults` without explicitly answering `package_name` or `coverage_threshold` will start failing. → Mitigation: this is the intended, documented **BREAKING** change; call it out prominently in the proposal and in this repo's own regression-suite invocations (already pass `-d package_name=...` explicitly in the "custom answers" scenario, and pass `-d project_name`/`-d author_name` in the "default answers" scenario — that scenario will need `-d package_name=...` and `-d coverage_threshold=...` added too).
- [Risk] `StrictUndefined` could surface latent undefined-variable bugs elsewhere in the template that previously rendered silently blank. → Mitigation: the full existing regression suite (`uv run pytest`) already exercises every templated file via real generations; running it after this change surfaces any such bug immediately, before merge.
