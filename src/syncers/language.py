# standard imports
import json

# external imports
from sqlalchemy.orm import Session

# local imports
from src.cache import cache_data, get_cached_data


def cache_supported_language(country_code: str, supported_languages: list):
    """This method caches the supported languages for a given country code.
    :param country_code: The country code for which the supported languages are cached.
    :type country_code: str
    :param supported_languages: The supported languages for the given country code.
    :type supported_languages: list
    """
    cache_data(key=country_code, data=json.dumps(supported_languages))


def get_cached_supported_languages(country_code: str):
    """This method retrieves the supported languages for a given country code.
    :param country_code: The country code for which the supported languages are cached.
    :type country_code: str
    :return: The supported languages for the given country code.
    :rtype: list
    """
    return json.loads(get_cached_data(country_code))
