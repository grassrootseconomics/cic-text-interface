# standard imports
import hashlib
import logging
from typing import Union

# external imports
from cic_types.condiments import MetadataPointer
from confini import Config
from redis import Redis, StrictRedis

# local imports
from src.condiments import CacheCondiments

logg = logging.getLogger(__file__)


class Cache:
    """
    This class exposes a singleton instance of a Redis client.
    """
    store: Redis = None


def initialize_cache(config: Config) -> None:
    """This function initializes the cache.
    :param config: The config object.
    :type config: Config
    """
    Cache.store = StrictRedis(host=config.get('REDIS_HOST'),
                              port=config.get('REDIS_PORT'),
                              password=config.get('REDIS_PASSWORD'),
                              db=config.get('REDIS_DATABASE'),
                              decode_responses=True)
    logg.debug('Initializing cache.')


def cache_data(key: str, data: Union[bytes, float, int, str]):
    """This function inserts data into the cache.
    :param key: A unique pointer.
    :type key: str
    :param data: A data object.
    :type data: Union[bytes, float, int, str]
    :return: None
    :rtype: None
    """
    cache = Cache.store
    cache.set(name=key, value=data)
    cache.persist(name=key)
    logg.debug(f'caching: {data} with key: {key}.')


def cache_data_key(identifier: Union[list, bytes], salt: Union[CacheCondiments, MetadataPointer]) -> str:
    """This function generates unique pointers by hashing the identifier and the salt.
    :param identifier: A list of bytes or a single bytes object.
    :type identifier: Union[list, bytes]
    :param salt: A condiment object.
    :type salt: CacheCondiments
    :return: A unique pointer.
    :rtype: str
    """
    hash_object = hashlib.new("sha256")
    if isinstance(identifier, list):
        for identity in identifier:
            hash_object.update(identity)
    else:
        hash_object.update(identifier)
    if salt != CacheCondiments.NONE:
        hash_object.update(salt.value.encode(encoding="utf-8"))
    return hash_object.digest().hex()


def get_cached_data(key: str) -> Union[bytes, float, int, str]:
    """This function retrieves data from the cache.
    :param key: A unique pointer.
    :type key: str
    :return: A data object.
    :rtype: Union[bytes, float, int, str]
    """
    cache = Cache.store
    return cache.get(name=key)
