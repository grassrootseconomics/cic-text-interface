# standard imports
import logging

# external imports
from celery import current_app

# local imports
from src.crud import (country as country_crud, supported_languages as supported_languages_crud)
from src.database.session import SessionLocal
from src.syncers.language import cache_supported_language

celery_app = current_app
logg = logging.getLogger()


@celery_app.task()
def sync_supported_languages():
    """
    This method syncs the cache of supported languages for all countries.
    """
    with SessionLocal() as db:
        countries = country_crud.get_multi(db)
        for country in countries:
            supported_languages = supported_languages_crud.get_country_supported_languages(db, country.id)
            supported_languages = [language.__dict__ for language in supported_languages]
            cache_supported_language(country.code, supported_languages)
