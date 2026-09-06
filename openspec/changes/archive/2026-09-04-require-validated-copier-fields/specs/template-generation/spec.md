## ADDED Requirements

### Requirement: Validated answer fields are required
Every `copier.yml` answer field that carries a `validator:` MUST be required (no `default:` key) unless the validator only applies conditionally to a non-empty value. `project_name`, `author_name`, `package_name`, and `coverage_threshold` MUST NOT have a `default:`. `author_email` MAY keep its `default: ""` because its validator only runs when a value is supplied. Fields without a `validator:` (`description`, `python_version`, `license`) MAY keep a `default:`.

#### Scenario: Generating without a required field fails
- **WHEN** a developer runs the Copier CLI non-interactively (e.g. `--defaults`) without supplying `project_name`, `author_name`, `package_name`, or `coverage_threshold`
- **THEN** Copier raises an error naming the missing question and does not generate a project

#### Scenario: Author email remains optional
- **WHEN** a developer runs the Copier CLI non-interactively without supplying `author_email`
- **THEN** Copier generates the project successfully using the empty default

### Requirement: Undefined template variables fail loudly
`copier.yml` MUST configure `_envops.undefined` so that any Jinja template variable left undefined during rendering raises an error instead of silently rendering as an empty string.

#### Scenario: Rendering with a missing variable errors
- **WHEN** a template file references a variable that has no value at render time (for example because the caller bypassed `copier.yml`'s question logic entirely)
- **THEN** rendering fails with an error rather than producing output containing a silently blank value
