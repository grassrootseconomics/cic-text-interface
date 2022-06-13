# external imports
from sqlalchemy import Column, Integer, ForeignKey

# local imports
from src.database.base_class import Base


class CountryLanguageAssociation(Base):
    country_id = Column(
        Integer,
        ForeignKey("country.id"),
        primary_key=True
    )

    language_id = Column(
        Integer,
        ForeignKey("language.id"),
        primary_key=True
    )
