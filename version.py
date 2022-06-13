# standard imports
import os

# external imports

# local imports

root_directory = os.path.dirname(__file__)
version_filepath = os.path.join(root_directory, 'VERSION')

with open(version_filepath, 'r') as version_file:
    version_lines = version_file.readlines()
    version = version_lines[0]

__version__ = str(version)
