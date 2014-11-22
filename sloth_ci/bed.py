from importlib import import_module
from os.path import abspath, join, exists
from os import makedirs

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

        self.api = API(self)

        self._setup_routing()
        
        log_dir = abspath(self.config.get('log_dir', '.'))
        
        if not exists(log_dir):
            makedirs(log_dir)
        
        cherrypy.config.update(
            {
                'environment': 'production',
                'server.socket_host': self.config['host'],
                'server.socket_port': self.config['port'],
                'log.access_file': join(log_dir, '_access.log'),
                'log.error_file': join(log_dir, '_error.log'),
            }
        )

        if config.get('daemon'):
            cherrypy.process.plugins.Daemonizer(self.bus).subscribe()

        self.bus.subscribe('stop', self.remove_all_sloths)

    def _setup_routing(self):
        '''Setup routing for API endpoint and app listeners.'''

        routes_dispatcher = cherrypy._cpdispatch.RoutesDispatcher()

        routes_dispatcher.connect('api', '/', self.api.listener)
        routes_dispatcher.connect('apps', '/{listen_point:.+}', self.listener)

        cherrypy.tree.mount(None, config={'/': {'request.dispatch': routes_dispatcher}})

    def start(self):
        '''Start CherryPy loop to listen for payload.'''

        self.bus.start()
        self.bus.block()

    def bind_config_file(self, listen_point, config_file):
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

    def add_sloth(self, config_string):
        '''Create a Sloth app from a config source and add it to the bed.

        :param config_string: a valid YAML config string

        :returns: new app's listen point
        '''

        config = load(config_string)

        try:
            listen_point = config['listen_point']

            if listen_point in self.sloths:
                raise ValueError(listen_point)

            ExtendedSloth, errors = Sloth.extend(config.get('extensions'))
            sloth = ExtendedSloth(config)

            for error in errors:
                sloth.logger.error(error)
            
            self.sloths[listen_point] = sloth
            sloth.logger.info('Listening on %s' % listen_point)

            cherrypy.log.error('Sloth app added, listening on %s' % listen_point)

            return listen_point

        except TypeError:
            cherrypy.log.error('Failed to create app: invalid config string')
            raise

        except KeyError as e:
            cherrypy.log.error('Failed to create app: the %s param is missing' % e)
            raise

        except ValueError as e:
            cherrypy.log.error('Failed to create app: the listen point %s is already taken' % e)
            raise

        except Exception as e:
            cherrypy.log.error('Failed to create app: %s' % e)
            raise

    def remove_sloth(self, listen_point):
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

    def remove_all_sloths(self):
        '''Stop all active Sloth apps and remove them from the bed.'''

        while self.sloths:
            listen_point, sloth = self.sloths.popitem()

            sloth.stop()
            self.config_files.pop(listen_point)

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