from models import GetDataError, GetDataResponse, RequestBody
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import status
import sql

from fastapi import APIRouter
from datetime import date
from utils import get_date_from_string

router = APIRouter()


@router.post(
    "/get_data",
    responses={
        status.HTTP_200_OK: {"model": GetDataResponse},
        status.HTTP_400_BAD_REQUEST: {"model": GetDataError},
    },
)
async def get_data(body: RequestBody) -> JSONResponse:
    from_date: date = get_date_from_string(body.from_date)
    to_date: date = get_date_from_string(body.to_date)
    result: dict = await sql.get_data(
        selected_columns=body.columns,
        filters=body.filters,
        dates=(from_date, to_date),
        group_columns=body.group_by,
        column_sort_by=body.order_by,
    )
    response: GetDataResponse = GetDataResponse(
        msg="Ok", status_code=status.HTTP_200_OK, data=result
    )
    return JSONResponse(
        content=jsonable_encoder(response),
        status_code=status.HTTP_200_OK,
        media_type="application/json",
    )
