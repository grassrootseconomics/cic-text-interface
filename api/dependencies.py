# standard imports
import logging
from typing import Generator

# local imports
from src.database.session import SessionLocal


logg = logging.getLogger(__file__)


def get_database() -> Generator:
    """
    This function exposes a generator that yields a database session object.
    :yield: A generator that yields a database session object.
    :rtype: Generator
    """
    database = SessionLocal()
    try:
        logg.debug('Retrieving database session.')
        yield database
    finally:
        logg.debug('Closing database session.')
        database.close()
