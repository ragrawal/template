## 1. Ruff docstring enforcement

- [x] 1.1 Add `"D"` to `select` and `[lint.pydocstyle] convention = "google"` in `templates/python-project/{{ package_name }}/ruff.toml.jinja`, and add `[lint.per-file-ignores]` `"tests/**" = ["D"]`; verify by generating a project and running `uv run poe lint` with no violations
- [x] 1.2 Add a one-line module docstring to `templates/ml/src/{{ package_name }}/tasks/__init__.py`; verify `uv run poe lint` reports no `D104` violation for that file in a generated project with the `ml` overlay applied

## 2. Pydantic `Field`-description convention in the `ml` overlay

- [x] 2.1 Update `templates/ml/webapp/app.py.jinja` so every field on `HealthResponse`, `HouseRecord`, `PredictRequest`, `Prediction`, and `PredictResponse` uses `Field(..., description="...")`; verify `uv run poe check --full` still passes in a generated project
- [x] 2.2 Add a reusable test helper (e.g. `assert_fields_documented`) that asserts every field of one or more Pydantic model classes has a non-empty `Field` description, placed alongside the `ml` overlay's test fixtures/helpers
- [x] 2.3 Call the helper from `templates/ml/tests/{{ package_name }}/test_schema.py` for `HouseFrame` and `HousePredictionData`, and from `templates/ml/tests/webapp/test_app.py` for `HealthResponse`, `HouseRecord`, `PredictRequest`, `Prediction`, and `PredictResponse`; verify `uv run poe test --full` passes and that reverting task 2.1 makes the new test fail

## 3. AGENTS.md guidance updates

- [x] 3.1 Add the "Document public classes and methods" (naming the Google docstring convention) and "Self-documenting Pydantic models" bullets to the Coding Principles list in `templates/python-project/{{ package_name }}/AGENTS.md.jinja`; verify by generating a project and checking the rendered `AGENTS.md` contains both bullets

## 4. Regression verification

- [x] 4.1 Run the full `templates/ml` overlay regression scenario end to end (`copier copy templates/python-project`, `copier copy templates/ml`, `uv sync`, `uv run poe check --full`) and confirm it exits `0` with the new lint rules and Field-description test enabled
- [x] 4.2 Run this repository's own `uv run pytest` (BDD regression suite) and confirm `tests/bdd/ml_overlay_test/ml_overlay_test.feature` still passes unchanged
