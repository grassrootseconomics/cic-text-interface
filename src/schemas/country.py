# standard imports
from typing import Optional, Union

# external imports
from pydantic import (BaseModel, constr)

# local imports
from .utils import ApiResponse


class CountryBase(BaseModel):
    code: constr(to_lower=True)
    name: str


class CountryCreate(CountryBase):
    code: constr(to_lower=True)
    name: str


class CountryUpdate(CountryBase):
    code: Union[constr(to_lower=True), None] = None
    name: Union[str, None] = None


# Properties shared by models stored in DB
class CountryInDBBase(CountryBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Country(CountryInDBBase):
    code = str
    name = str


# Properties stored in DB
class CountryInDB(CountryInDBBase):
    pass


class CountryApiResponse(ApiResponse):
    data: Optional[Country] = None
