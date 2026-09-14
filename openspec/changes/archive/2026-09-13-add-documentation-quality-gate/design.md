## Context

`ruff.toml.jinja` (bundled by `templates/python-project`, shared unchanged by
the `ml` overlay) currently selects `["E", "F", "I", "UP", "B"]` — no
docstring rules. Existing bundled source (`schema.py`, `estimator.py.jinja`,
`train_model.py.jinja`, `app.py.jinja`) is already well-documented, except
`tasks/__init__.py` (empty, no docstring). Test files across both templates
have no docstrings by convention — `AGENTS.md` already instructs the
assistant to favor descriptive `pytest.param(..., id=...)` names over a
docstring per case.

`schema.py`'s `HouseFrame`/`HousePredictionData` already use
`Field(description=...)` for every field. `webapp/app.py.jinja`'s five
`BaseModel` subclasses (`HealthResponse`, `HouseRecord`, `PredictRequest`,
`Prediction`, `PredictResponse`) use bare type annotations instead. There is
no ruff (or other static) rule that can check "every Pydantic field has a
`Field` description" — this requires a runtime/test-level check.

See proposal.md for motivation.

## Goals / Non-Goals

**Goals:**
- Make missing docstrings on public classes/functions a lint failure
  (`uv run poe lint` / `check`), without breaking the existing bundled
  scaffold or the existing testing convention (descriptive test names, no
  per-test docstrings).
- Make every bundled Pydantic model in the `ml` overlay self-documenting via
  `Field(..., description=...)`, and add an automated, reusable check that
  catches a future regression.
- Update `AGENTS.md` so an AI assistant applies both conventions by default
  when writing new code in a generated project.

**Non-Goals:**
- Do not enforce docstrings on private (`_`-prefixed) helpers or on test
  functions — matches the project's existing testing convention.
- Do not build a custom ruff/AST plugin for the `Field`-description check;
  a pytest-level check is sufficient and keeps the tool count unchanged.
- Do not change coverage thresholds, type-checking, or any other unrelated
  `quality-check-task` behavior.
- Do not add pydocstyle enforcement to the meta-repo (this repository's own
  `AGENTS.md`/tooling) — scope is the templates' generated output only.

## Decisions

**Docstring convention: ruff `D` rules with `convention = "google"`.**
Setting `[lint.pydocstyle] convention = "google"` alongside adding `"D"` to
`select` auto-resolves the mutually exclusive `D203`/`D211` and
`D212`/`D213` pairs for that convention, so no manual ignore list is needed
for those. Google is chosen over `numpy`/`pep257` because it's the
convention already implicitly followed by the bundled docstrings (one-line
summary, no rigid section headers) — no rewrite of existing docstrings is
needed.

**Test files are exempted via `per-file-ignores`, not by writing docstrings
on every test.** Alternative considered: require `D103` (missing
docstring in public function) everywhere, including tests. Rejected because
`AGENTS.md` already establishes descriptive test names + `pytest.param(...,
id=...)` as the way tests document intent, and retrofitting a docstring onto
every test function would fight that convention rather than reinforce it.
`ruff.toml.jinja` will add:
```toml
[lint.per-file-ignores]
"tests/**" = ["D"]
```

**`tasks/__init__.py` gets a one-line module docstring** rather than a
blanket `D104` ignore for `__init__.py` files, since `src/__init__.py.jinja`
already carries one (`"""{{ package_name }}."""`) — consistent treatment,
smallest diff, no new ignore rule to maintain.

**`Field`-description enforcement is a pytest check, not a ruff rule.**
Ruff has no rule for "a Pydantic field lacks a `Field(description=...)`."
Add a small, reusable assertion helper (e.g.
`assert_fields_documented(*model_classes)` iterating
`model_cls.model_fields` and checking `.description` is truthy) used by the
existing `test_schema.py` (for `HouseFrame`, `HousePredictionData`) and
`test_app.py` (for the five webapp models). This keeps the check inside the
test suite the project already runs via `uv run poe check`, rather than
introducing a new tool or a new `poe` task.

**Fix `webapp/app.py.jinja`'s models directly** rather than leaving them
non-compliant and only adding the check — the check should start green.

## Risks / Trade-offs

- [Risk] Enabling `D` rules could surface additional violations in generated
  code beyond what was inspected here (e.g. if a future edit to the base
  template adds an undocumented public function) → Mitigation: the
  regression suite already runs `uv run poe check` against a freshly
  generated project (including the `ml` overlay) as part of
  `template-regression-testing`, so any new violation is caught immediately
  after this change lands, not discovered by a downstream consumer.
- [Risk] `google` convention docstring formatting is stricter about sections
  like `Args:`/`Returns:` if they're partially present → Mitigation: none of
  the bundled docstrings currently use structured sections (they're
  one-line summaries), so this does not apply today; call out the
  convention in `AGENTS.md` so future docstrings stay compatible.
- [Trade-off] The `Field`-description check is enforced only where a test
  file already exists (schema + webapp models) — it is a convention
  reinforced by `AGENTS.md` and a template-level test, not a repo-wide
  static guarantee for every possible future Pydantic model a developer
  might add. Acceptable because ruff has no equivalent static rule to fall
  back on, and the goal is to catch regressions in the bundled models, not
  to police arbitrary user-authored models after generation.
