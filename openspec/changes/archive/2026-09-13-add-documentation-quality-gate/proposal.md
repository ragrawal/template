# Proposal: Add Documentation Quality Gate

## Why

Generated projects currently have no automated check that public classes and
methods are documented, and no enforced convention that Pydantic model fields
are declared with `Field(..., description=...)`. The `ml` overlay's
`schema.py` already follows the `Field`-with-description pattern, but the
webapp's request/response models (`HealthResponse`, `HouseRecord`,
`PredictRequest`, `Prediction`, `PredictResponse`) do not, and nothing in the
`lint` step or `AGENTS.md` guidance would catch a future regression in either
project's source or in future models added to either template.

## What Changes

- **Ruff docstring enforcement**: add pydocstyle (`D`) rules to the shared
  `ruff.toml.jinja` bundled by `templates/python-project` (and inherited by
  the `ml` overlay), with a `convention` setting and per-file exemptions for
  `tests/` (tests already document intent via descriptive names, per existing
  `AGENTS.md` guidance, not docstrings).
- **Pydantic `Field`-with-description convention**: document the convention
  in `AGENTS.md`'s Coding Principles, fix the `ml` overlay's webapp models to
  follow it, and add an automated, reusable test check (since no ruff rule
  covers this) that fails if any bundled Pydantic model's fields are missing
  a `Field` description.
- **`AGENTS.md` updates**: add the two conventions above as coding
  principles so an AI assistant follows them by default in both the
  `python-project` and `ml` templates.
- Fix the `ml` overlay's `tasks/__init__.py` (currently empty) and any other
  currently-undocumented public module needed to pass the new lint rules
  cleanly once generated.

## Impact

- Affected specs: `quality-check-task` (lint step rule set), `ai-agent-guidance`
  (Coding Principles), `ml` (webapp models, generated test suite)
- Affected code: `templates/python-project/{{ package_name }}/ruff.toml.jinja`,
  `templates/python-project/{{ package_name }}/AGENTS.md.jinja`,
  `templates/ml/webapp/app.py.jinja`,
  `templates/ml/src/{{ package_name }}/tasks/__init__.py`,
  `templates/ml/tests/**` (new/updated field-documentation checks)
- No answer-schema changes; no migration needed.
