## ADDED Requirements

### Requirement: Pydantic models are self-documenting via Field descriptions
Every Pydantic `BaseModel` field bundled by the `ml` overlay (in `schema.py` and in the webapp's request/response models in `webapp/app.py`) MUST be declared using `pydantic.Field` with a non-empty `description`, so the model's JSON schema documents each field without relying on external documentation. The generated project MUST include an automated check, run as part of its test suite (and therefore as part of `uv run poe check`), that fails if any of these bundled models declares a field without a `Field` description.

#### Scenario: Webapp request/response models declare Field descriptions
- **WHEN** a project is generated with the `ml` overlay
- **THEN** every field on `HealthResponse`, `HouseRecord`, `PredictRequest`, `Prediction`, and `PredictResponse` in `webapp/app.py` is declared via `Field(..., description=...)` with a non-empty description

#### Scenario: Missing field description fails the test suite
- **WHEN** a bundled Pydantic model's field is declared without a `Field` description (for example, during future maintenance of the template)
- **THEN** the generated project's test suite fails, identifying which model and field lacks a description
