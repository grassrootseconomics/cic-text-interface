# standard imports
import logging

# external imports
from confini import Config

logg = logging.getLogger()


def data_source_name_from_config(config: Config):
    """This function builds a data source name mapping to a database from values defined in the config object.
    :param config: A config object.
    :type config: Config
    :return: A database URI.
    :rtype: str
    """
    scheme = config.get('DATABASE_ENGINE')
    if config.get('DATABASE_DRIVER') is not None:
        scheme += f"+{config.get('DATABASE_DRIVER')}"

    if config.get('DATABASE_ENGINE') == 'sqlite':
        data_source_name = f'{scheme}:///{config.get("DATABASE_NAME")}'

    else:
        data_source_name = f"{scheme}://{config.get('DATABASE_USER')}:{config.get('DATABASE_PASSWORD')}@{config.get('DATABASE_HOST')}:{config.get('DATABASE_PORT')}/{config.get('DATABASE_NAME')}"

    logg.debug(f'parsed dsn from config: {data_source_name}')
    return data_source_name
