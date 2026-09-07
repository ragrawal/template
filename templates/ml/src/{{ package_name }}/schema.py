"""Pydantic schemas for the house-price feature set and model predictions."""

from __future__ import annotations

from typing import Annotated, Any, Self

import numpy as np
import numpy.typing as npt
from pydantic import BaseModel, Field, GetCoreSchemaHandler, model_validator
from pydantic_core import core_schema


class _NumpyArraySchema:
    """Pydantic annotation that validates/coerces a value into a numpy.ndarray of a fixed dtype.

    Lists/tuples are coerced via ``np.asarray``; an existing ndarray is checked
    against ``dtype`` and copied if it doesn't already match.
    """

    def __init__(self, dtype: npt.DTypeLike) -> None:
        self._dtype = np.dtype(dtype)

    def __get_pydantic_core_schema__(
        self, source_type: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        def validate(value: Any) -> np.ndarray:
            try:
                return np.asarray(value, dtype=self._dtype)
            except (TypeError, ValueError) as exc:
                raise ValueError(
                    f"Cannot coerce value to numpy array of dtype {self._dtype}: {exc}"
                ) from exc

        return core_schema.no_info_plain_validator_function(
            validate,
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda arr: arr.tolist()
            ),
        )


Float64Array = Annotated[np.ndarray, _NumpyArraySchema(np.float64)]
BoolArray = Annotated[np.ndarray, _NumpyArraySchema(np.bool_)]
ObjectArray = Annotated[np.ndarray, _NumpyArraySchema(object)]


class PyDanticDataFrame(BaseModel):
    """A pydantic model whose fields are equal-length numpy arrays, addressable like columns."""

    @model_validator(mode="after")
    def validate_count(self) -> Self:
        """Validate that all fields have the same length."""
        lengths = [len(getattr(self, field)) for field in type(self).model_fields]
        if len(set(lengths)) > 1:
            raise ValueError("All fields must have the same length")
        return self

    def __len__(self) -> int:
        """Return the number of rows."""
        return len(getattr(self, next(iter(type(self).model_fields))))


class HouseFrame(PyDanticDataFrame):
    """Features for the California-housing-shaped house-price dataset."""

    med_inc: Float64Array = Field(
        description="Median income in block group (tens of thousands of dollars)"
    )
    house_age: Float64Array = Field(description="Median house age in block group (years)")
    ave_rooms: Float64Array = Field(description="Average number of rooms per household")
    ave_bedrms: Float64Array = Field(description="Average number of bedrooms per household")
    population: Float64Array = Field(description="Block group population")
    ave_occup: Float64Array = Field(description="Average number of household members")
    latitude: Float64Array = Field(description="Block group latitude")
    longitude: Float64Array = Field(description="Block group longitude")


class HousePredictionData(PyDanticDataFrame):
    """Predictions produced by the house-price estimator."""

    price: Float64Array = Field(description="Predicted median house value")
    is_valid: BoolArray = Field(description="Whether the prediction looks plausible (price > 0)")
    info: ObjectArray = Field(
        description="Additional per-prediction information (reserved for future use)"
    )
