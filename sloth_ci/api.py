﻿from importlib import import_module

from sys import exit

from os.path import isdir, isfile, abspath, join, exists
from os import listdir, makedirs, stat

from argparse import ArgumentParser

import cherrypy
from configs import load

from .sloth import Sloth


def make_extended_sloth(extensions):
    '''Sequentially chain-inherit Sloth classes from extensions.
    
    The first extension's Sloth class inherits from the base Sloth class and becomes the base class, then the second one inherits from it, and so on.

    :params extensions: list of extensions to load.
    
    :returns: ExtendedSloth—a Sloth class inherited from all extensions' Sloth classes; errors—list of errors raised during the extensions loading.
    '''
    
    ExtendedSloth = Sloth
    errors = []

    if extensions:
        for extension in extensions:
            try:
                ext = import_module('.ext.%s' % extension, package=__package__)
            
                ExtendedSloth = ext.extend(ExtendedSloth)

            except Exception as e:
                errors.append('Could not load extension %s: %s' % (extension, e))

    return ExtendedSloth, errors


def get_config_files(config_locations):
    '''Generate a list of config files for Sloth apps.

    :param config_locations: file and dir paths to config files.

    :returns: tuple of config file set and config directory set
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


def make_listener(sloth):
    '''Creates a listener function for a Sloth app.

    :param sloth: Sloth app.
    '''

    @cherrypy.expose
    def listener(*args, **kwargs):
        '''Listens to requests.

        :param payload: payload
        '''

        sloth.logger.info('Payload received from %s - %s' % (cherrypy.request.headers['Remote-Addr'], cherrypy.request.headers['User-Agent']))

        try:
            validator = import_module(
                '.validators.%s' % sloth.config['provider'],
                package=__package__
            )
        except ImportError as e:
            sloth.logger.critical('No matching validator found: %s' % e)
            raise cherrypy.HTTPError(500, 'No matching validator found: %s' % e)

        provider_data = sloth.config.get('provider_data') or {}

        validation_status, validation_message, validator_params = validator.validate(cherrypy.request, provider_data)

        custom_params = sloth.config.get('params')

        if custom_params:
            custom_params = custom_params.dict_props

        else:
            custom_params = {}

        custom_params.update(validator_params)

        params = custom_params

        sloth.logger.info(validation_message.format_map(validator_params))

        if validation_status != 200:
            raise cherrypy.HTTPError(validation_status, validation_message.format_map(validator_params))

        if not sloth.is_queue_locked():
            sloth.queue.append(params)

    return listener


class ConfigChecker(cherrypy.process.plugins.Monitor):
    def __init__(self, bus, config_files, config_dirs, frequency=5):
        self.config_files = config_files
        self.config_dirs = config_dirs

        print('self.config_files, self.config_dirs ', self.config_files, self.config_dirs)

        super().__init__(bus, self.check, frequency)

    def start(self):
        if not self.thread:
            self.mtimes = {}
        self.mtimes = {}

        print('mtimes', self.mtimes)

        super().start()

    def check(self):
        print('Check')

        config_files, config_dirs = get_config_files(self.config_files | self.config_dirs)

        print('oldfiles', self.config_files)
        print('newfiles', config_files)

        for config_file in config_files - self.config_files:
            cherrypy.engine.publish('app-add', config_file)

        for config_file in self.config_files - config_files:
            cherrypy.engine.publish('app-remove', config_file)
            self.mtimes.pop(config_file)

        for config_file in config_files:
            mtime = stat(config_file).st_mtime
            print(mtime)

            if not config_file in self.mtimes:
                self.mtimes[config_file] = mtime

            elif mtime > self.mtimes[config_file]:
                cherrypy.engine.publish('app-update', config_file)
                self.mtimes[config_file] = mtime

        self.config_files, self.config_dirs = config_files, config_dirs


def run(host, port, log_dir, config_files, config_dirs, sconfig_file, sloths):
    '''Runs CherryPy loop to listen for payload.

    :param host: host
    :param port: port
    :param log_dir: directory to store logs (absolute or relative)
    :param sloths: list of Sloth apps to run
    '''

    cherrypy.config.update(
        {
            'server.socket_host': host,
            'server.socket_port': port,
            'log.access_file': abspath(join(log_dir, '_access.log')),
            'log.error_file': abspath(join(log_dir, '_error.log')),
            'request.show_tracebacks': False,
            'request.show_mismatched_params': False
        }
    )
     
    cherrypy.engine.autoreload.files.add(abspath(sconfig_file))

    #for dir in config_dirs:
    #    cherrypy.engine.autoreload.files.add(abspath(dir))

    for sloth in sloths:
        try:
            sloth.start()

            cherrypy.tree.mount(make_listener(sloth), sloth.config['listen_to'])

            sloth.logger.info('Mounted at %s' % sloth.config['listen_to'])

            #cherrypy.engine.autoreload.files.add(sloth.config.config_full_path)

            cherrypy.engine.subscribe('stop', sloth.stop)

        except:
            pass

    config_checker = ConfigChecker(cherrypy.engine, config_files, config_dirs)

    config_checker.subscribe()

    cherrypy.engine.subscribe('app-add', test_add)
    cherrypy.engine.subscribe('app-remove', test_remove)
    cherrypy.engine.subscribe('app-update', test_update)

    cherrypy.engine.start()
    cherrypy.engine.block()


def test_add(config_file):
    print('Add ', config_file)

def test_remove(config_file):
    print('Remove ', config_file)

def test_update(config_file):
    print('Update ', config_file)

def main():
    '''Main API function.'''

    parser = ArgumentParser()
    parser.add_argument('--sconfig', help='Server config.')
    parser.add_argument('--host', help='Host for the Sloth server (overrides value in sconfig).')
    parser.add_argument('--port', type=int, help='Port for the Sloth server (overrides value in sconfig).')
    parser.add_argument('--log_dir', help='Where the log files should be stored (overrides value in sconfig).')
    parser.add_argument('config', nargs='+', help='Sloth app config files or dirs.')

    parsed_args = parser.parse_args()

    sconfig_file = parsed_args.sconfig

    if sconfig_file:
        sconfig = load(sconfig_file)
    else:
        sconfig = {}

    host = parsed_args.host or sconfig.get('host')
    port = parsed_args.port or sconfig.get('port')
    log_dir = parsed_args.log_dir or sconfig.get('log_dir')

    if not (host and port and log_dir):
        exit('Missing server param(s).')

    config_locations = parsed_args.config

    config_files, config_dirs = get_config_files(config_locations)

    if not exists(abspath(log_dir)):
        makedirs(abspath(log_dir))

    sloths = []

    for config_file in config_files:
        try:
            config = load(config_file)

            ExtendedSloth, errors = make_extended_sloth(config.get('extensions'))

            extended_sloth = ExtendedSloth(config)

            for error in errors:
                extended_sloth.logger.error(error)

            sloths.append(extended_sloth)
        
        except Exception as e:
            print('Could not load Sloth app config %s: %s' % (config_file, e))

    run(host, port, log_dir, config_files, config_dirs, sconfig_file, sloths)