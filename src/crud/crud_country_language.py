# standard imports
from typing import List

# external imports
from sqlalchemy.orm import Session

# local imports
from src.crud.base import CRUDBase
from src.models.language import Language
from src.models.country_langauge_association import CountryLanguageAssociation
from src.schemas.country_language import CountryLanguageCreate, CountryLanguageUpdate


class CRUDCountry(CRUDBase[CountryLanguageAssociation, CountryLanguageCreate, CountryLanguageUpdate]):

    def get_country_supported_languages(self, db: Session, country_id: int):
        return db.query(Language.id, Language.name, Language.symbol)\
            .join(self.model)\
            .filter(self.model.country_id == country_id)\
            .all()


supported_languages = CRUDCountry(CountryLanguageAssociation)
