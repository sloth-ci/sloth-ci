from importlib import import_module

from os.path import abspath, exists, dirname
from os import makedirs
from glob import glob

import logging

import cherrypy

from yaml import load

from .sloth import Sloth
from .api.server import API


class Bed:
    '''A container for Sloth apps.

    It tracks their config files and listen points, as well as handles app adding, removing and updating.

    If also implements the listen function for the main CherryPy app.

    (This module is names "bed" because a group of sloth is actually called "bed".)
    '''

    def __init__(self, config):
        '''Configure CherryPy loop to listen for payload.

        :param config: bed config
        '''

        self.config = config
        self.bus = cherrypy.engine

        self.sloths = {}
        self.config_files = {}

        self._configure()
        self._setup_routing()

    def _setup_routing(self):
        '''Setup routing for API endpoint and app listeners.'''

        routes_dispatcher = cherrypy._cpdispatch.RoutesDispatcher()

        routes_dispatcher.connect('api', '/', self.api.listener)
        routes_dispatcher.connect('apps', '/{listen_point:.+}', self.listener)

        cherrypy.tree.mount(None, config={'/': {'request.dispatch': routes_dispatcher}})

    def _configure(self):
        '''Configure CherryPy server.'''

        self.db_path = self.config.get('paths', {}).get('db', 'sloth.db')

        if self.db_path:
            db_dir = dirname(abspath(self.db_path))

            if db_dir and not exists(db_dir):
                makedirs(db_dir)

            self.db_extensions = {
                'db_app_logs': {
                    'module': 'db_app_logs',
                    'db': self.db_path,
                    'table': 'app_logs'
                },
                'db_build_history': {
                    'module': 'db_build_history',
                    'db': self.db_path,
                    'table': 'build_history'
                }
            }

        access_log_path = self.config.get('paths', {}).get('access_log', 'sloth_access.log')
        access_log_dir = dirname(access_log_path)

        if access_log_dir and not exists(access_log_dir):
            makedirs(access_log_dir)

        error_log_path = self.config.get('paths', {}).get('error_log', 'sloth_error.log')
        error_log_dir = dirname(error_log_path)

        if error_log_dir and not exists(error_log_dir):
            makedirs(error_log_dir)

        cherrypy.config.update(
            {
                'environment': 'production',
                'server.socket_host': self.config['host'],
                'server.socket_port': self.config['port'],
                'log.access_file': access_log_path,
                'log.error_file': error_log_path
            }
        )

        if self.config.get('daemon'):
            cherrypy.process.plugins.Daemonizer(self.bus).subscribe()

        self.bus.subscribe('stop', self.remove_all)

        self.api = API(self)

    def autocreate(self):
        '''Create apps before server start.
        
        The app configs are extracted from the files defined in the config_paths section of the server config.
        '''

        for config_path in self.config.get('paths', {}).get('configs', []):
            config_files = glob(config_path)

            if not config_files:
                cherrypy.log.error('Path %s not found' % config_path)
                continue

            for config_file in config_files:
                try:
                    config = load(open(config_file))

                    listen_point = self.create(config)

                    self.bind(listen_point, abspath(config_file))

                except:
                    continue

    def start(self):
        '''Start CherryPy loop to listen for payload.'''

        self.autocreate()

        self.bus.start()
        self.bus.block()

    def bind(self, listen_point, config_file):
        '''Bind a Sloth app with a config file.

        :param listen_point: app's listen point
        :param config_file: absolute path to the config file
        '''

        try:
            sloth = self.sloths[listen_point]

            if sloth.config == load(open(config_file)):
                self.config_files[listen_point] = config_file
                sloth.logger.info('Bound with config file %s' % config_file)

                cherrypy.log.error('App on %s bound with config file %s' % (listen_point, config_file))

            else:
                raise ValueError

        except KeyError:
            cherrypy.log.error('Failed to bind config file: listen point %s not found' % listen_point)
            raise

        except FileNotFoundError:
            cherrypy.log.error('Failed to bind config file: file %s not found' % config_file)
            raise

        except ValueError:
            cherrypy.log.error('Failed to bind config file: config mismatch')
            raise

    def create(self, config):
        '''Create a Sloth app from a config source and add it to the bed.

        :param config: a dict parsed from YAML

        :returns: new app's listen point
        '''

        try:
            listen_point = config['listen_point']

        except TypeError:
            cherrypy.log.error('Failed to create app: invalid config string')
            raise

        except KeyError:
            cherrypy.log.error('Failed to create app: the listen_point param is missing' % e)
            raise

        if listen_point in self.sloths:
            cherrypy.log.error('Failed to create app: the listen point %s is already taken' % listen_point)
            raise ValueError(listen_point)

        try:
            if self.db_path:
                PreExtendedSloth, errors = Sloth.extend(self.db_extensions)

            else:
                PreExtendedSloth, errors = Sloth

            ExtendedSloth, errors = PreExtendedSloth.extend(config.get('extensions'))
            sloth = ExtendedSloth(config)

            for error in errors:
                sloth.logger.error(error)

            self.sloths[listen_point] = sloth
            sloth.logger.info('Listening on %s' % listen_point)

            cherrypy.log.error('Sloth app added, listening on %s' % listen_point)

            return listen_point

        except Exception as e:
            cherrypy.log.error('Failed to create app: %s' % e)
            raise

    def remove(self, listen_point):
        '''Stop Sloth app and remove it from the bed.

        :param listen_point: Sloth app listen point
        '''

        try:
            self.sloths.pop(listen_point).stop()

            self.config_files.pop(listen_point, None)

            cherrypy.log.error('Sloth app at %s removed' % listen_point)

        except KeyError:
            cherrypy.log.error('Failed to remove app: listen point %s not found' % listen_point)
            raise

        except Exception as e:
            cherrypy.log.error('Failed to remove app on %s: %s' % (listen_point, e))

    def remove_all(self):
        '''Stop all active Sloth apps and remove them from the bed.'''

        while self.sloths:
            listen_point, sloth = self.sloths.popitem()

            sloth.stop()

            self.config_files.pop(listen_point, None)

    @cherrypy.expose
    @cherrypy.tools.proxy()
    def listener(self, listen_point, **kwargs):
        '''Listens for payloads and routes them to the responsible Sloth app.

        :param listen_point: Sloth app listen point (part of the URL after the server host)
        '''

        sloth = self.sloths.get(listen_point)

        if sloth:
            sloth.handle(cherrypy.request)

        else:
            raise cherrypy.HTTPError(404, 'This listen point does not exist.')