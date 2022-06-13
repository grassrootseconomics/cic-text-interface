# standard imports
import argparse
import os

# external imports
from celery import Celery
from confini import Config

# local imports
from src.cache import initialize_cache
from src.worker.celery_utils import create_celery_app
from tasks import *

logging.basicConfig(level=logging.WARNING)
logg = logging.getLogger()
logging.getLogger('gnupg').setLevel(logging.WARNING)

config_directory = '/usr/local/etc/cic-ussd/'

# define arguments
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-c', type=str, default=config_directory, help='config directory.')
arg_parser.add_argument('-q', type=str, default='cic-ussd', help='queue name for worker tasks')
arg_parser.add_argument('-v', action='store_true', help='be verbose')
arg_parser.add_argument('-vv', action='store_true', help='be more verbose')
arg_parser.add_argument('--env-prefix', default=os.environ.get('CONFINI_ENV_PREFIX'), dest='env_prefix', type=str,
                        help='environment prefix for variables to overwrite configuration')
args = arg_parser.parse_args()

# define log levels
if args.vv:
    logging.getLogger().setLevel(logging.DEBUG)
elif args.v:
    logging.getLogger().setLevel(logging.INFO)

# parse config
config = Config(args.c, args.env_prefix)
config.process()
config.add(args.q, '_CELERY_QUEUE', True)
config.censor('PASSWORD', 'DATABASE')
logg.debug('config loaded from {}:\n{}'.format(args.c, config))

current_app = Celery(__name__)
create_celery_app(config)

initialize_cache(config)


def main():
    argv = ['worker']
    if args.vv:
        argv.append('--loglevel=DEBUG')
    elif args.v:
        argv.append('--loglevel=INFO')
    argv.extend(('-Q', args.q, '-n', args.q))
    current_app.worker_main(argv)


if __name__ == '__main__':
    main()
