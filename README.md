# Python Project Copier Template

A [Copier](https://copier.readthedocs.io/) template for bootstrapping installable
Python projects (`src`-layout, hatchling build backend) with `uv` for dependency
management, `ruff` (lint/format), `pyright` (type checking), `pytest`+`pytest-cov`
(tests/coverage), and [Poe the Poet](https://poethepoet.natehaus.co/) as the task
runner. Generated projects ship a GitHub Actions quality workflow and bundled AI
agent guidance (`AGENTS.md` + a Claude Code skill).

## Using this template

Generate a new project from it:

```bash
uv tool run copier copy <this-repo-url-or-path>/templates/python-project path/to/new-project
```

This creates the generated project at `path/to/new-project/<package_name>/`, not
directly in `path/to/new-project/` — the template always nests its output under a
folder named after the answered `package_name`.

Answer the prompts (package name, Python version) or pass `--data key=value` /
`--defaults` to skip them. See
[`specs/001-python-project-template/quickstart.md`](specs/001-python-project-template/quickstart.md)
for a full worked example.

To pull in template updates later, run `copier update` inside the generated project.

## Developing this template

The template source lives under [`templates/python-project/`](templates/python-project/)
(each file, aside from `copier.yml`, mirrors what a generated project receives).
[`templates/python-project/copier.yml`](templates/python-project/copier.yml) defines the prompts.

This repository has its own dependencies (`copier`, `pytest`, `pytest-bdd`) for
testing the template itself — install them with `uv sync`, then run the
regression suite:

```bash
uv run pytest
```

The suite (`tests/bdd/`) generates a real project from the current template
source via the `copier copy` CLI, installs its dependencies, and runs its
quality checks — so a breaking change to the template is caught here before it
reaches downstream consumers.

See [`specs/001-python-project-template/`](specs/001-python-project-template/) for
the full spec, plan, and task breakdown behind this template.
