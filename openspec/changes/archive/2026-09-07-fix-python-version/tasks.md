## 1. Fix the post-generation task

- [x] 1.1 In `templates/python-project/copier.yml`, change the `_tasks` entry from a bare command string to the dict form with `command: "uv python pin {{ python_version }}"` and `working_directory: "{{ package_name }}"`
- [x] 1.2 Generate a project into a scratch directory (e.g. `copier copy templates/python-project <tmp-dest>`) and verify `.python-version` exists inside `<tmp-dest>/<package_name>/` and matches the answered `python_version`, and that no `.python-version` file was created at `<tmp-dest>` root

## 2. Verify against the spec

- [x] 2.1 Run `openspec validate --changes fix-python-version --strict` and confirm it passes
