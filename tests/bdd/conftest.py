"""Shared fixtures for this repository's own pytest-bdd regression suite.

This suite exercises the template by shelling out to real CLI commands (never
Copier's internal Python API or other in-process shortcuts), so it fails the
same way a real downstream consumer's commands would.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

# Shared step definitions become conftest fixtures visible to the whole
# tests/bdd subtree (pytest-bdd's documented sharing pattern): pytest-bdd's
# @given/@when/@then decorators inject each step's fixture into the module
# where the decorator is literally written, so importing these modules here
# (a conftest.py, which pytest scans directly for fixtures) is what registers
# them -- not the plain function names the star-import also brings in.
from tests.bdd.actions.files import *  # noqa: E402,F403
from tests.bdd.actions.shell import *  # noqa: E402,F403

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


@pytest.fixture
def repo_root() -> Path:
    """The root of this repository (templates live under templates/<name>/)."""
    return REPO_ROOT


@pytest.fixture(autouse=True)
def clean_working_tree() -> None:
    """Every regression run must leave this repository's working tree unchanged.

    Generated projects and broken-template copies only ever live under pytest's
    `tmp_path`, outside this repository, so a before/after `git status` snapshot of
    this repository should be identical regardless of what this run generates.
    """

    def snapshot() -> str:
        result = subprocess.run(
            ["git", "status", "--porcelain", "--", "."],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        return result.stdout

    before = snapshot()
    yield
    after = snapshot()
    assert before == after, (
        "A regression run left this repository's working tree changed.\n"
        f"Before:\n{before}\nAfter:\n{after}"
    )
