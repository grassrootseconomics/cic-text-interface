# local imports
from src.crud.base import CRUDBase
from src.models.country import Country
from src.schemas.country import CountryCreate, CountryUpdate


class CRUDCountry(CRUDBase[Country, CountryCreate, CountryUpdate]):

    ...


country = CRUDCountry(Country)
