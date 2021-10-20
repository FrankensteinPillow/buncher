from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel, Field, validator

from sql import ALL_COLUMNS, NOT_NUMERIC_COLS
from utils import get_date_from_string


class RequestBody(BaseModel):
    columns: List[str] = Field(
        list(ALL_COLUMNS),
        title="Selected columns",
        description="Columns displayed in the final selection.",
    )
    filters: List[Tuple[str, str]] = Field(
        [],
        title="Selection filter list",
        description=(
            "The filter list is represented by the column name and the "
            "compared value. The comparison operation is only available for "
            "strict equality so far."
        ),
    )
    from_date: str = Field(
        "0001-01-01",
        title="Start date filter",
        description="Start date of filtering date range. Can be 'inf'",
    )
    to_date: str = Field(
        "9999-12-31",
        description="End date filter",
        title="End date of filtering date range. Can be 'inf'",
    )
    order_by: Tuple[str, str] = Field(
        (None, None),
        title="Order by column",
        description=(
            "The column by which the values will be sorted. The second value "
            "can be specified flags for sorting in descending (desc) and "
            "ascending (asc) order"
        ),
    )
    group_by: List[str] = Field(
        [],
        title="Group by columns",
        description="Columns by which values will be grouped",
    )

    @validator("columns")
    def columns_validator(cls, values: List[str]) -> List[str]:
        for value in values:
            if value != "CPI" and value not in ALL_COLUMNS:
                raise ValueError(f"Column '{value}' can not be selected")
        return values

    @validator("filters")
    def filters_validator(
        cls, values: List[Tuple[str, str]]
    ) -> List[Tuple[str, str]]:
        for value in values:
            if value[0] not in NOT_NUMERIC_COLS:
                raise ValueError(
                    f"Selection results can not be filterred by column "
                    f"'{value[0]}'"
                )
        return values

    @validator("from_date")
    def from_date_validator(cls, value: str) -> str:
        if value == "inf":
            return "0001-01-01"
        try:
            get_date_from_string(value)
        except ValueError:
            raise ValueError(
                "Invalid format of date. Date should be represented in "
                "YYYY-MM-DD format or 'inf'"
            )
        return value

    @validator("to_date")
    def to_date_validator(cls, value: str) -> str:
        if value == "inf":
            return "9999-12-31"
        try:
            get_date_from_string(value)
        except ValueError:
            raise ValueError(
                "Invalid format of date. Date should be represented in "
                "YYYY-MM-DD format or 'inf'"
            )
        return value

    @validator("order_by")
    def order_by_validator(cls, value: Tuple[str, str]) -> Tuple[str, str]:
        if isinstance(value, tuple):
            if value[0] != "CPI" and value[0] not in ALL_COLUMNS:
                raise ValueError(f"Column '{value[0]}' not found")
            if len(value) == 2:
                if value[1] not in ("asc", "desc"):
                    raise ValueError("Must be 'asc' or 'desc'")
                return value
            return value[0], "asc"
        else:
            if value != "CPI" and value not in ALL_COLUMNS:
                raise ValueError(f"Column '{value}' not found")
            return value, "asc"

    @validator("group_by")
    def group_by_validator(
        cls, values: Optional[List[str]]
    ) -> Optional[List[str]]:
        if values is None:
            return values
        for value in values:
            if value not in NOT_NUMERIC_COLS:
                raise ValueError(f"Can not be grouped by column '{value}'")
        return values


class GetDataResponse(BaseModel):
    msg: str
    status_code: int
    data: List[Dict[str, Any]]


class GetDataError(BaseModel):
    msg: str
    status_code: int
