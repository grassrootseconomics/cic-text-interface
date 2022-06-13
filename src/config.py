# standard imports
import logging
import os

# external imports
from confini import Config

# local import

src_directory = os.path.dirname(__file__)
root_directory = os.path.dirname(src_directory)
default_config_directory = os.path.join(root_directory, 'config')

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()

config_directory = os.environ.get("CONFIG_DIR") or default_config_directory
logg.debug(f"Loading configs from: {config_directory}")

# process configs
config = Config(config_directory)
config.process()
config.censor('PASSWORD', 'DATABASE')
logg.debug(f'config:\n{config}')
