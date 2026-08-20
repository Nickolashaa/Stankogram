from typing import Any

from sqlalchemy import Select, func, select


def _get_count_stmt(stmt: Select[tuple[Any]]) -> Select[tuple[int]]:
    return select(func.count()).select_from(stmt.subquery())
