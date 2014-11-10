from sys import platform
from os.path import isdir, isfile, join, abspath, expanduser
from os import listdir, stat
from cherrypy.process.plugins import Monitor

from yaml import load


def get_configs(location):
    '''Recursively get all config files from a ceratin location (can be a directory or a single file).
    
    :param location: path to a directory or config file
    '''

    if isfile(location):
        try:
            yield load(open(location))

        except:
            pass

    elif isdir(location):
        for item in (join(location, _) for _ in listdir(location)):
            yield from get_configs(item)