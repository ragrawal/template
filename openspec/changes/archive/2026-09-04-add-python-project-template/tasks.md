## 1. Project context

- [x] 1.1 Write `openspec/project.md` covering purpose, tech stack, and conventions, sourced from `README.md`, `specs/001-python-project-template/spec.md` (Assumptions), and `plan.md`/`research.md` (Technical Context and decisions) — verified the file exists and names the actual tech stack (uv, ruff, pyright, pytest, Poe the Poet, Copier, hatchling, GitHub Actions)

## 2. Retire Spec Kit tooling

- [x] 2.1 Delete `.specify/` (scripts, templates, workflows, manifests) — verified `.specify/` no longer exists
- [x] 2.2 Delete `specs/001-python-project-template/` (superseded by `openspec/specs/{template-generation,quality-check-task,pr-quality-gate,ai-agent-guidance,template-regression-testing}/`) — verified the directory (and now-empty parent `specs/`) no longer exists
- [x] 2.3 Delete the ten `.claude/skills/speckit-*/` command skill directories — verified `.claude/skills/` contains no `speckit-*` entries

## 3. Validate the migration

- [x] 3.1 Run `openspec validate add-python-project-template --strict` and resolve any reported issues — passed
- [x] 3.2 Confirm no remaining references to `/speckit-*` commands, `.specify/`, or `specs/001-python-project-template/` outside of git history (`grep -rIl speckit` across the repo, excluding `.git`) — only remaining hits are historical mentions inside this change's own `proposal.md`/`design.md`/`tasks.md`
