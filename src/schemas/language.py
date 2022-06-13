# standard imports
from typing import Optional, Union

# external imports
from pydantic import (BaseModel, constr)

# local imports
from .utils import ApiResponse


class LanguageBase(BaseModel):
    name: str
    symbol: constr(to_lower=True)


class LanguageCreate(LanguageBase):
    name: str
    symbol: constr(to_lower=True)


class LanguageUpdate(LanguageBase):
    name: Union[str, None] = None
    symbol: Union[constr(to_lower=True), None] = None


# Properties shared by models stored in DB
class LanguageInDBBase(LanguageBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Language(LanguageInDBBase):
    name: str
    symbol: str


# Properties stored in DB
class LanguageInDB(LanguageInDBBase):
    pass


class LanguageApiResponse(ApiResponse):
    data: Optional[Language] = None
