from typing import List, Dict, Any, Set, Tuple, Optional

import databases as db
from databases.core import Database
import sqlalchemy
from sqlalchemy import Date, Table
from sqlalchemy.sql import select
from sqlalchemy.sql.schema import MetaData, Column
from sqlalchemy import and_, func, text
from sqlalchemy.sql.selectable import Select, Subquery

from config import get_config, Config
from datetime import date

CONFIG: Config = get_config()
NUMERIC_COLS: Set = {"impressions", "clicks", "installs", "spend", "revenue"}
NOT_NUMERIC_COLS: Set = {"date", "channel", "country", "os"}
ALL_COLUMNS: Set = NUMERIC_COLS | NOT_NUMERIC_COLS

database: Database = db.Database(CONFIG.db_url)
metadata: MetaData = sqlalchemy.MetaData()
dataset: Table = Table(
    "dataset",
    metadata,
    sqlalchemy.Column("date", Date),
    sqlalchemy.Column("channel", sqlalchemy.TEXT),
    sqlalchemy.Column("country", sqlalchemy.TEXT),
    sqlalchemy.Column("os", sqlalchemy.TEXT),
    sqlalchemy.Column("impressions", sqlalchemy.INTEGER),
    sqlalchemy.Column("clicks", sqlalchemy.INTEGER),
    sqlalchemy.Column("installs", sqlalchemy.INTEGER),
    sqlalchemy.Column("spend", sqlalchemy.FLOAT),
    sqlalchemy.Column("revenue", sqlalchemy.FLOAT),
)


def _selected_columns(columns: List[str]) -> List[Column]:
    return [dataset.c[name] for name in columns] if columns else []


def _filter_by_date(query: Select, dates: Tuple[date]) -> Select:
    if dates:
        query: Select = query.where(
            and_(
                dataset.c.date >= dates[0], dataset.c.date <= dates[1]
        ))
    return query

def _filter_by_value(query: Select, filters: List[Tuple[str, str]]) -> Select:
    for f in filters:
        query = query.where(dataset.c[f[0]] == f[1])
    return query

def _select_agregate_columns(
    columns: List[str], group_columns: List[str]
) -> List[Column]:
    if not group_columns:
        return []
    return _selected_columns(set(columns) & NUMERIC_COLS)


def _get_selected_columns(
    selected: List[str], all_columns: List[Column]
) -> List[Column]:
    return [c for c in all_columns if c.name in selected]


async def get_data(
    selected_columns: List[str],
    filters: List[Tuple[str, str]],
    dates: Tuple[str, str],
    group_columns: Optional[List[str]],
    column_sort_by: Tuple[str, str],
) -> List[Dict[str, Any]]:
    columns: List[str] = [c.name for c in dataset.columns]
    agregate_cols: List[Column] = _select_agregate_columns(
        columns, group_columns
    )
    group_columns: List[Column] = _selected_columns(group_columns)
    columns: List[Column] = _selected_columns(columns)
    for c in agregate_cols:
        columns.remove(c)
        columns.append(func.sum(c).label(c.name))
    query: Select = select(
        *columns,
    ).group_by(*group_columns)
    query = _filter_by_date(query, dates)
    query = _filter_by_value(query, filters)
    if "CPI" in selected_columns:
        sbqry: Subquery = query.subquery("main_table")
        query = select(
            *sbqry.columns, (sbqry.c.spend / sbqry.c.installs
        ).label("CPI"))
    order: str = column_sort_by[0]
    if column_sort_by[1]:
        order = text(f"{column_sort_by[0]} {column_sort_by[1]}")
    query = query.order_by(order)
    sbqry: Subquery = query.subquery("all_data")
    query = select(*_get_selected_columns(selected_columns, sbqry.columns))
    rows = await database.fetch_all(query)
    return [dict(r) for r in rows]
