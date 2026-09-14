## Why

The `python-project` template's post-generation task runs `uv python pin` in Copier's destination directory, not inside the generated project's `{{ package_name }}` folder. Because this template nests all generated content under `{{ package_name }}/`, the resulting `.python-version` file lands one level above where the project actually lives, so the project itself is left unpinned.

## What Changes

- Fix the `_tasks` entry in `templates/python-project/copier.yml` so `uv python pin {{ python_version }}` runs with its working directory set to the generated `{{ package_name }}/` folder instead of the Copier destination root.
- Clarify the `template-generation` spec's Python-version-pinning scenario to state explicitly that the `.python-version` file must be written inside the generated `package_name` project directory, not the destination path passed to Copier — closing the ambiguity that let this bug pass unnoticed.

## Capabilities

### New Capabilities
(none)

### Modified Capabilities
- `template-generation`: The "Generated project pins its Python version" requirement's scenario is tightened to assert the `.python-version` file's location is inside the `package_name` project folder, not merely "the generated project."

## Impact

- `templates/python-project/copier.yml` (`_tasks` definition)
- Any project already generated with this bug will have a stray `.python-version` at the destination root and none inside the project folder; users will need to regenerate or manually run `uv python pin` inside the project folder (not part of this change's scope, but worth calling out during rollout).
