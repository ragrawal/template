"""Reusable file/content step definitions shared across feature files."""

from __future__ import annotations

import shutil
from pathlib import Path

import yaml
from pytest_bdd import given, parsers, then, when

from tests.bdd.actions.shell import resolve


@given("a copy of the template source with a broken ruff configuration")
def given_broken_template_source(tmp_dir: Path, repo_root: Path) -> None:
    template_dir = repo_root / "templates" / "python-project"
    broken_dir = tmp_dir / "broken-template"
    shutil.copytree(template_dir, broken_dir)
    ruff_config = broken_dir / "{{ package_name }}" / "ruff.toml.jinja"
    ruff_config.write_text(ruff_config.read_text() + "\n[unterminated-section\n")


@then(parsers.parse("the following files exist: {file_list}"))
def then_files_exist(file_list: str, repo_root: Path, tmp_dir: Path) -> None:
    for raw_path in file_list.split(","):
        path = Path(resolve(raw_path.strip(), repo_root, tmp_dir))
        assert path.is_file(), f"missing {path}"


@then(parsers.parse("the following files do not exist: {file_list}"))
def then_files_do_not_exist(file_list: str, repo_root: Path, tmp_dir: Path) -> None:
    for raw_path in file_list.split(","):
        path = Path(resolve(raw_path.strip(), repo_root, tmp_dir))
        assert not path.exists(), f"unexpectedly found {path}"


@then(parsers.parse('no "{dirname}" directories exist under "{path}"'))
def then_no_directories_exist(
    dirname: str, path: str, repo_root: Path, tmp_dir: Path
) -> None:
    root = Path(resolve(path, repo_root, tmp_dir))
    matches = list(root.rglob(dirname))
    assert not matches, f"found unexpected {dirname} director(y/ies): {matches}"


@then(parsers.parse('the file "{path}" contains "{text}"'))
def then_file_contains(path: str, text: str, repo_root: Path, tmp_dir: Path) -> None:
    resolved_path = Path(resolve(path, repo_root, tmp_dir))
    assert resolved_path.is_file(), f"missing {resolved_path}"
    assert text in resolved_path.read_text()


@then(parsers.parse('the file "{path}" does not contain "{text}"'))
def then_file_does_not_contain(
    path: str, text: str, repo_root: Path, tmp_dir: Path
) -> None:
    resolved_path = Path(resolve(path, repo_root, tmp_dir))
    assert resolved_path.is_file(), f"missing {resolved_path}"
    assert text not in resolved_path.read_text()


@given(parsers.parse('the content of "{path}" is remembered'), target_fixture="remembered_content")
def given_content_remembered(path: str, repo_root: Path, tmp_dir: Path) -> bytes:
    resolved_path = Path(resolve(path, repo_root, tmp_dir))
    return resolved_path.read_bytes()


@then(parsers.parse('the file "{path}" still matches the remembered content'))
def then_file_matches_remembered_content(
    path: str, repo_root: Path, tmp_dir: Path, remembered_content: bytes
) -> None:
    resolved_path = Path(resolve(path, repo_root, tmp_dir))
    assert resolved_path.read_bytes() == remembered_content


@then(
    parsers.parse(
        'the quality workflow at "{path}" is triggered on pull request open and synchronize'
    )
)
def then_quality_workflow_is_valid(path: str, repo_root: Path, tmp_dir: Path) -> None:
    workflow_path = Path(resolve(path, repo_root, tmp_dir))
    workflow = yaml.safe_load(workflow_path.read_text())
    # PyYAML parses the bare `on:` key as the boolean key `True`.
    triggers = workflow.get("on", workflow.get(True))
    pull_request_types = triggers["pull_request"]["types"]
    assert "opened" in pull_request_types
    assert "synchronize" in pull_request_types
