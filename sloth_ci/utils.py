from sys import platform
from os.path import isdir, isfile, join, abspath, expanduser
from os import listdir, stat
from cherrypy.process.plugins import Monitor


def get_default_configs_path():
    '''Get the path to the configs depending on the current OS.'''

    if platform == 'win32':
        return abspath(expanduser('~/AppData/Local/sloth-ci/configs'))
    elif platform == 'linux':
        return abspath('/etc/sloth-ci/configs')


def get_default_logs_path():
    '''Get the logs dir path depending on the current OS.'''

    if platform == 'win32':
        return abspath(expanduser('~/AppData/Local/sloth-ci/logs'))
    elif platform == 'linux':
        return abspath('/var/log/sloth-ci')


def get_config_files(config_locations):
    '''Generate a set of config files and config directories for Sloth apps.

    :param config_locations: file and dir paths to config files.

    :returns: tuple of a config file set and a config directory set
    '''

    config_files = set()
    config_dirs = set()

    for location in config_locations:
        if isfile(location):
            config_files.add(location)
        elif isdir(location):
            config_dirs.add(location)

            for item in (join(location, _) for _ in listdir(location)):
                if isfile(item):
                    config_files.add(item)
    
    return config_files, config_dirs


class ConfigChecker(Monitor):
    '''Monitor-based CherryPy plugin that tracks file and directory modifications, additions, and deletions.

    On each event, it publishes a respective signal.
    '''

    def __init__(self, bus, config_locations, frequency=1):
        self.config_locations = config_locations

        self.config_files, self.config_dirs = set(), set()

        super().__init__(bus, self.check, frequency)

    def start(self):
        self.mtimes = {}

        super().start()

    def check(self):
        new_config_files, new_config_dirs = get_config_files(self.config_locations)

        for config_file in new_config_files - self.config_files:
            self.bus.publish('sloth-add', config_file)

        for config_file in self.config_files - new_config_files:
            self.bus.publish('sloth-remove', config_file)
            self.mtimes.pop(config_file)

        for config_file in new_config_files:
            mtime = stat(config_file).st_mtime

            if not config_file in self.mtimes:
                self.mtimes[config_file] = mtime

            elif mtime > self.mtimes[config_file]:
                self.bus.publish('sloth-update', config_file)
                self.mtimes[config_file] = mtime

        self.config_files, self.config_dirs = new_config_files, new_config_dirs
        self.config_locations = self.config_files | self.config_dirs
