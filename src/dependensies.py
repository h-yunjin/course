from typing import Annotated
from fastapi import Depends, Query

from pydantic import BaseModel

class Pagination(BaseModel):
    page: Annotated[int | None, Query(None, gt=0)]
    per_page: Annotated[int | None, Query(None, gt=0, lt=30)]

PaginationDep = Annotated[Pagination, Depends()]    