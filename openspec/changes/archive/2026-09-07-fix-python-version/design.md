## Context

Copier tasks (`_tasks`) run with their working directory relative to `subproject.local_abspath` (the destination path passed to `copier copy`), defaulting to that root when unset. This template nests all generated content under `{{ package_name }}/` rather than generating directly into the destination, so the current bare-string task `"uv python pin {{ python_version }}"` runs in the destination root and writes `.python-version` one level above the actual project. See `proposal.md` - Why.

Copier (pinned at `>=9.18.1` in this repo's `uv.lock`) supports a dict form for `_tasks` entries with `command` and `working_directory` keys; `working_directory` is resolved relative to the destination path and defaults to `.` when omitted.

## Goals / Non-Goals

**Goals:**
- Ensure `uv python pin` executes inside the generated `{{ package_name }}/` directory so `.python-version` lands with the rest of the project.

**Non-Goals:**
- Cleaning up `.python-version` files stray from prior (buggy) generations - that's a per-user follow-up, not something this template can retroactively fix.
- Changing the `python_version` answer schema, choices, or default.

## Decisions

**Use the dict form of `_tasks` with an explicit `working_directory`, instead of embedding `cd` in the command string.**

```yaml
_tasks:
  - command: "uv python pin {{ python_version }}"
    working_directory: "{{ package_name }}"
```

Alternatives considered:
- `cmd: "cd {{ package_name }} && uv python pin {{ python_version }}"` - works on POSIX shells but is less portable (relies on `&&` semantics under `use_shell`) and mixes concerns (directory navigation with the actual command) in one string.
- Moving all template content to the destination root and dropping the `{{ package_name }}/` nesting - rejected as out of scope; it would be a much larger structural change affecting the answers-file location and every other templated path, well beyond this bug fix.

The dict form is native to Copier's task model, keeps the working directory declaration explicit and separate from the command, and needs no shell-specific quoting.

## Risks / Trade-offs

- [Existing generated projects still have a stray root-level `.python-version` and none inside the project folder] → Not fixable retroactively by this change; call out in release/changelog notes that affected users should regenerate or run `uv python pin` manually inside their project folder.
