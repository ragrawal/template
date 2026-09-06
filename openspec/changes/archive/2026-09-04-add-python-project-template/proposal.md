## Why

This repository is migrating from GitHub Spec Kit to OpenSpec. The Spec Kit feature `specs/001-python-project-template/` (spec, plan, tasks, research, data model, contracts, quickstart) describes a Copier template for bootstrapping Python projects, and every task in it is already implemented and shipped. OpenSpec needs an initial baseline that reflects that shipped behavior so future changes to the template have real specs to diff against, instead of starting from an empty `openspec/specs/` tree.

## What Changes

- Establish `openspec/project.md` as the project's context document (tech stack, conventions, constraints), replacing the never-ratified `.specify/memory/constitution.md`.
- Add five new capabilities to `openspec/specs/`, each capturing already-implemented, still-current behavior of this repository's Copier template:
  - `template-generation`
  - `quality-check-task`
  - `pr-quality-gate`
  - `ai-agent-guidance`
  - `template-regression-testing`
- Retire the Spec Kit tooling this repository used to author the above: `.specify/` (scripts, templates, workflows, manifests), `specs/001-python-project-template/` (superseded by the specs below), and the `.claude/skills/speckit-*/` command skills. **BREAKING** for any workflow that still invokes `/speckit-*` commands or reads files under `.specify/` or `specs/`.

## Capabilities

### New Capabilities
- `template-generation`: Copier answer-schema prompts and the templated project tree they render (dependency manager, per-tool config files, packaging, project-hygiene files) that let a separate repository bootstrap a fully-tooled Python project from this template.
- `quality-check-task`: The single Poe the Poet `check` task (plus its `format`/`lint`/`typecheck`/`test` sub-tasks) bundled into every generated project, running formatting, type-checking, and coverage-enforced tests with one pass/fail result.
- `pr-quality-gate`: The GitHub Actions workflow bundled into every generated project that runs the quality-check task automatically when a pull request is opened and on every subsequent push to it.
- `ai-agent-guidance`: The `AGENTS.md` guidance file and the bundled `.claude/skills/run-quality-checks` functional skill shipped in every generated project.
- `template-regression-testing`: This repository's own `pytest-bdd` suite and push-triggered GitHub Actions workflow that generate a real project from the current template and exercise its CLI commands, so a breaking template change is caught immediately.

### Modified Capabilities
(none — this is the initial OpenSpec baseline; no capabilities exist yet under `openspec/specs/`)

## Impact

- **Added**: `openspec/project.md`; `openspec/specs/{template-generation,quality-check-task,pr-quality-gate,ai-agent-guidance,template-regression-testing}/spec.md`.
- **Removed**: `.specify/` (entire directory), `specs/001-python-project-template/` (entire directory), `.claude/skills/speckit-*/` (10 command skill directories).
- **Unaffected**: The actual shipped artifacts these specs describe — `copier.yml`, `template/`, `tests/`, `.github/workflows/template-regression.yml` — no code or template output changes as part of this migration.
