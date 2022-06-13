# standard imports
from typing import Any, Optional, TypeVar, Union

# external imports
from pydantic import BaseModel

ModelSchemaType = TypeVar("ModelSchemaType", bound=BaseModel)


class ApiResponse(BaseModel):
    message: str
    status: int


class Paginate(BaseModel):
    values: Optional[list[Union[ModelSchemaType, Any]]] = None  # type: ignore
    total: Optional[int] = 0
    prev_link: Optional[str] = None
    next_link: Optional[str] = None
