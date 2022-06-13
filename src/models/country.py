# external imports
from sqlalchemy import Column, Integer, String

# local imports
from src.database.base_class import Base


class Country(Base):
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)

    def country_object(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name
        }
