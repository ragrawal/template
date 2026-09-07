Feature: Python project template generation
  This repository's templates/python-project Copier template must keep
  producing a working, installable Python project as the template itself
  evolves (template-regression-testing capability).

  Scenario: Generate a project with default answers
    Given a temporary directory
    When the user runs "uv tool run copier copy {repo_root}/templates/python-project {tmp_dir}/project --data package_name=demo --defaults --trust"
    Then the following files exist: {tmp_dir}/project/demo/AGENTS.md, {tmp_dir}/project/demo/pyproject.toml
    And the following files exist: {tmp_dir}/project/demo/.answers/.python_project.yml
    And the following files do not exist: {tmp_dir}/project/demo/.copier-answers.yml
    And no "__pycache__" directories exist under "{tmp_dir}/project"
    When the user runs "uv sync" in "{tmp_dir}/project/demo"
    Then the command exits with code 0
    When the user runs "uv run poe check" in "{tmp_dir}/project/demo"
    Then the command exits with code 0

  Scenario: Generate a project with custom answers
    Given a temporary directory
    When the user runs "uv tool run copier copy {repo_root}/templates/python-project {tmp_dir}/project --data package_name=custom_widgets --data python_version=3.11 --defaults --trust"
    Then the following files exist: {tmp_dir}/project/custom_widgets/AGENTS.md, {tmp_dir}/project/custom_widgets/pyproject.toml
    And no "__pycache__" directories exist under "{tmp_dir}/project"
    When the user runs "uv sync" in "{tmp_dir}/project/custom_widgets"
    Then the command exits with code 0
    When the user runs "uv run poe check" in "{tmp_dir}/project/custom_widgets"
    Then the command exits with code 0

  Scenario: A broken template produces a clear failure
    Given a temporary directory
    And a copy of the template source with a broken ruff configuration
    When the user runs "uv tool run copier copy {tmp_dir}/broken-template {tmp_dir}/project --data package_name=demo --defaults --trust"
    Then the command exits with code 0
    When the user runs "uv run poe check" in "{tmp_dir}/project/demo"
    Then the command exits with a non-zero code
    And the output contains "ruff"

  Scenario: Each Poe the Poet task follows its exit-code contract
    Given a temporary directory
    When the user runs "uv tool run copier copy {repo_root}/templates/python-project {tmp_dir}/project --data package_name=demo --defaults --trust"
    And the user runs "uv sync" in "{tmp_dir}/project/demo"
    Then the command exits with code 0
    When the user runs "uv run poe format" in "{tmp_dir}/project/demo"
    Then the command exits with code 0
    When the user runs "uv run poe lint" in "{tmp_dir}/project/demo"
    Then the command exits with code 0
    When the user runs "uv run poe typecheck" in "{tmp_dir}/project/demo"
    Then the command exits with code 0
    When the user runs "uv run poe test" in "{tmp_dir}/project/demo"
    Then the command exits with code 0
    When the user runs "uv run poe test --full" in "{tmp_dir}/project/demo"
    Then the command exits with code 0
    When the user runs "uv run poe check" in "{tmp_dir}/project/demo"
    Then the command exits with code 0
    When the user runs "uv run poe check --full" in "{tmp_dir}/project/demo"
    Then the command exits with code 0

  Scenario: The generated project ships a valid PR-triggered quality workflow
    Given a temporary directory
    When the user runs "uv tool run copier copy {repo_root}/templates/python-project {tmp_dir}/project --data package_name=demo --defaults --trust"
    Then the following files exist: {tmp_dir}/project/demo/.github/workflows/quality.yml
    And the quality workflow at "{tmp_dir}/project/demo/.github/workflows/quality.yml" is triggered on pull request open and synchronize

  Scenario: The generated project ships AI agent guidance and a quality-check skill
    Given a temporary directory
    When the user runs "uv tool run copier copy {repo_root}/templates/python-project {tmp_dir}/project --data package_name=demo --defaults --trust"
    Then the following files exist: {tmp_dir}/project/demo/AGENTS.md, {tmp_dir}/project/demo/.claude/skills/run-quality-checks/SKILL.md
    And the file "{tmp_dir}/project/demo/AGENTS.md" contains "uv run poe check"
    And the file "{tmp_dir}/project/demo/AGENTS.md" contains "Domain-model-first"
    And the file "{tmp_dir}/project/demo/AGENTS.md" contains "pytest.mark.parametrize"
    And the file "{tmp_dir}/project/demo/AGENTS.md" contains "pytest.param"
    And the file "{tmp_dir}/project/demo/AGENTS.md" contains "time/space complexity"
    And the file "{tmp_dir}/project/demo/.claude/skills/run-quality-checks/SKILL.md" contains "uv run poe check"

  Scenario: Missing package_name fails generation
    Given a temporary directory
    When the user runs "uv tool run copier copy {repo_root}/templates/python-project {tmp_dir}/project --defaults --trust"
    Then the command exits with a non-zero code
    And the output contains "package_name"

  Scenario: Passing --full to check runs the complete suite with coverage enforced
    Given a temporary directory
    When the user runs "uv tool run copier copy {repo_root}/templates/python-project {tmp_dir}/project --data package_name=demo --defaults --trust"
    And the user runs "uv sync" in "{tmp_dir}/project/demo"
    Then the command exits with code 0
    When the user runs "uv run poe check --full" in "{tmp_dir}/project/demo"
    Then the command exits with code 0
    And the output contains "tests coverage"

  Scenario: Default check run selects tests via testmon
    Given a temporary directory
    When the user runs "uv tool run copier copy {repo_root}/templates/python-project {tmp_dir}/project --data package_name=demo --defaults --trust"
    And the user runs "uv sync" in "{tmp_dir}/project/demo"
    Then the command exits with code 0
    When the user runs "uv run poe check" in "{tmp_dir}/project/demo"
    Then the command exits with code 0
    And the output contains "testmon"

  Scenario: Generated project has no LICENSE and no description or authors metadata
    Given a temporary directory
    When the user runs "uv tool run copier copy {repo_root}/templates/python-project {tmp_dir}/project --data package_name=demo --defaults --trust"
    Then the following files do not exist: {tmp_dir}/project/demo/LICENSE
    And the file "{tmp_dir}/project/demo/pyproject.toml" does not contain "description ="
    And the file "{tmp_dir}/project/demo/pyproject.toml" does not contain "authors"
    And the file "{tmp_dir}/project/demo/pyproject.toml" does not contain "[project.license]"
    And the file "{tmp_dir}/project/demo/README.md" contains "# demo"
