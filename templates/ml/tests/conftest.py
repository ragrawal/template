"""Shared pytest fixtures for the ml overlay's test suite."""

from collections.abc import Callable

import pytest
from pydantic import BaseModel


@pytest.fixture
def assert_fields_documented() -> Callable[..., None]:
    """Return a helper asserting every field of the given model classes has a description."""

    def _assert_fields_documented(*model_classes: type[BaseModel]) -> None:
        for model_cls in model_classes:
            for field_name, field_info in model_cls.model_fields.items():
                assert field_info.description, (
                    f"{model_cls.__name__}.{field_name} is missing a Field(description=...)"
                )

    return _assert_fields_documented
