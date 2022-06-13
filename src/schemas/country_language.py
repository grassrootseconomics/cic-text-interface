# standard imports
from typing import Optional
from datetime import datetime

# external imports
from pydantic import BaseModel

# local imports
from .language import Language
from .utils import ApiResponse


# Shared properties
class CountryLanguageBase(BaseModel):
    country_id: Optional[int] = None
    language_id: Optional[int] = None


# Properties to receive on item creation
class CountryLanguageCreate(CountryLanguageBase):
    country_id: int
    language_id: int


# Properties to receive on item update
class CountryLanguageUpdate(CountryLanguageBase):
    pass


# Properties shared by models stored in DB
class CountryLanguageInDBBase(CountryLanguageUpdate):

    class Config:
        orm_mode = True


# Properties to return to client
class CountryLanguage(CountryLanguageInDBBase):
    pass


# Properties stored in DB
class CountryLanguageInDB(CountryLanguageInDBBase):
    created_at: datetime
    updated_at: datetime


class CountryLanguageApiResponse(ApiResponse):
    data: Optional[Language] = None
