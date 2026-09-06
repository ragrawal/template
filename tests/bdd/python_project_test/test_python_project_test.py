"""Binds python_project_test.feature to the shared action-module step definitions.

Step definitions live in tests.bdd.actions.shell / tests.bdd.actions.files and
are registered as fixtures by the wildcard imports in tests/bdd/conftest.py.
This file only binds the feature.
"""

from __future__ import annotations

from pytest_bdd import scenarios

scenarios("python_project_test.feature")
