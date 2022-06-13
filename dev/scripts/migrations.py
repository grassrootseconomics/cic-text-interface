# standard imports
import logging
import os
import sys
from argparse import ArgumentParser

# external imports
import alembic
from alembic.config import Config as AlembicConfig
from confini import Config

# local imports
from src.database import data_source_name_from_config

logging.basicConfig(level=logging.WARNING)
logg = logging.getLogger()

dev_directory = os.path.dirname(os.path.dirname(__file__))
root_directory = os.path.dirname(dev_directory)

default_config_directory = os.path.join(root_directory, 'config')

db_directory = os.path.join(root_directory, 'src', 'database')
migrations = os.path.join(db_directory, 'migrations')

arg_parser = ArgumentParser(description='CLI for handling cic-ussd server applications.')
arg_parser.add_argument('-c', type=str, default=default_config_directory, help='config root to use')
arg_parser.add_argument('-v', help='be verbose', action='store_true')
arg_parser.add_argument('-vv', help='be more verbose', action='store_true')
arg_parser.add_argument('--migrations-dir', dest='migrations_dir', default=migrations, type=str,
                        help='path to alembic migrations directory')

subcommand = sys.argv[1:][0]
# TODO[Philip]: You might want to find a cleaner way of doing this.
args = arg_parser.parse_args(sys.argv[1:][1:])

# define log levels
if args.vv:
    logging.getLogger().setLevel(logging.DEBUG)
elif args.v:
    logging.getLogger().setLevel(logging.INFO)

# process configs
config = Config(args.c)
config.process()
config.censor('PASSWORD', 'DATABASE')
logg.debug(f'config:\n{config}')

# define data source name
data_source_name = data_source_name_from_config(config)

# define migration configs
migrations_dir = os.path.join(args.migrations_dir, config.get('DATABASE_ENGINE'))
if not os.path.isdir(migrations_dir):
    logg.debug(f'migrations dir for engine {config.get("DATABASE_ENGINE")} not found, reverting to default')
    migrations_dir = os.path.join(args.migrations_dir, 'default')

logg.info(f'using migrations dir {migrations_dir}')
logg.info(f'using db {data_source_name}')

# define alembic configs
alembic_config = AlembicConfig(os.path.join(migrations_dir, 'alembic.ini'))
alembic_config.set_main_option('sqlalchemy.url', data_source_name)
alembic_config.set_main_option('script_location', migrations_dir)


def revision():
    alembic.command.revision(alembic_config, autogenerate=True)


def migrate():
    alembic.command.upgrade(alembic_config, 'head')


# process "subcommand"
execute = None
if subcommand == "revision":
    execute = revision
elif subcommand == 'migrate':
    execute = migrate
else:
    raise IOError("Unsupported migration subcommand.")

if __name__ == '__main__':
    try:
        execute()
    except (ValueError, AttributeError) as error:
        logg.error(f'An error occurred: {error}.')
        sys.exit(1)
