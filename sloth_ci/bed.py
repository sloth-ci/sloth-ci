from importlib import import_module
from os.path import abspath, join, exists
from os import makedirs

import logging

import cherrypy

from yaml import load

from .sloth import Sloth
from .api import API


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

        self.listen_points = {}

        self.api = API(self)

        self._setup_routing()
        
        log_dir = abspath(self.config['log_dir'])
        
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

    def add_sloth(self, config_source):
        '''Create a Sloth app from a config source and add it to the bed.

        :param config_source: a file object, a path to a file, or a config string
        '''

        try:
            config = load(open(config_source))

        except:
            config = load(config_source)

        try:
            listen_point = config['listen_point']

            if listen_point in self.listen_points:
                raise ValueError(listen_point)

            ExtendedSloth, errors = Sloth.extend(config.get('extensions'))
            sloth = ExtendedSloth(config)

            for error in errors:
                sloth.logger.error(error)
            
            self.listen_points[listen_point] = sloth
            sloth.logger.info('Listening on %s' % listen_point)

            cherrypy.log.error('Sloth app added, listening on %s' % listen_point)

            return listen_point

        except KeyError as e:
            cherrypy.log.error('Could not add Sloth app from the config source %s: the %s param is missing' % (config_source, e))
            raise

        except ValueError as e:
            cherrypy.log.error('Could not add Sloth app from the config source %s: the listen point %s is already taken' % (config_source, e))
            raise

        except Exception as e:
            cherrypy.log.error('Could not add Sloth app from the config source %s: %s' % (config_source, e))
            raise

    def remove_sloth(self, listen_point):
        '''Stop Sloth app and remove it from the bed.

        :param listen_point: Sloth app listen point
        '''

        try:
            if not listen_point in self.listen_points:
                raise KeyError(listen_point)

            self.listen_points.pop(listen_point).stop()

            cherrypy.log.error('Sloth app at %s removed' % listen_point)

            return listen_point
 
        except Exception as e:
            cherrypy.log.error('Could not remove Sloth app on the listen point %s: %s' % (listen_point, e))
            raise

    def remove_all_sloths(self):
        '''Stop all active Sloth apps and remove them from the bed.'''

        while self.listen_points:
            self.listen_points.popitem()[1].stop()

    @cherrypy.expose
    @cherrypy.tools.proxy()
    def listener(self, listen_point, **kwargs):
        '''Listens for payloads and routes them to the responsible Sloth app.

        :param listen_point: Sloth app listen point (part of the URL after the server host)
        '''

        sloth = self.listen_points.get(listen_point)

        if sloth:
            sloth.handle(cherrypy.request)

        else:
            raise cherrypy.HTTPError(404, 'This listen point does not exist.')