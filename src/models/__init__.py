# standard imports
from glob import glob
from importlib import import_module
from os.path import basename, dirname, isfile, join

modules = glob(join(dirname(__file__), "*.py"))

for file in modules:
    # exclude 'init.py'
    if isfile(file) and not file.endswith("__init__.py"):
        # strip .py extension
        file_name = basename(file[:-3])
        import_module(f".{file_name}", package=__name__)
