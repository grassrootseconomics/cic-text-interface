# external imports
from sqlalchemy import Column, Integer, String

# local imports
from src.database.base_class import Base


class Language(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    symbol = Column(String, unique=True, nullable=False)
