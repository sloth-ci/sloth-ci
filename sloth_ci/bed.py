from importlib import import_module
from os.path import abspath, join
import logging

import cherrypy

from yaml import load

from .sloth import Sloth
from .utils import ConfigChecker
from .api import API


class Bed:
    '''A container for Sloth apps.

    It tracks their config files and listen points, as well as handles app adding, removing and updating.

    If also implements the listen function for the main CherryPy app.

    (This module is names "bed" because a group of sloth is actually called "bed".)
    '''
    
    def __init__(self, sconfig):
        '''Configure CherryPy loop to listen for payload.

        :param sconfig: bed config
        '''

        self.sconfig = sconfig
        self.bus = cherrypy.engine

        self.config_files = {}
        self.listen_points = {}

        self.api = API(self)

        routes_dispatcher = cherrypy._cpdispatch.RoutesDispatcher()
        routes_dispatcher.connect('api', '/', self.api.listener)
        routes_dispatcher.connect('apps', '/{listen_to:.+}', self.listener)

        cherrypy.tree.mount(None, config={
            '/': {
                'request.dispatch': routes_dispatcher,
            }
        })

        cherrypy.config.update(
            {
                'environment': 'production',
                'server.socket_host': sconfig['host'],
                'server.socket_port': sconfig['port'],
                'log.access_file': abspath(join(sconfig['paths']['logs'], '_access.log')),
                'log.error_file': abspath(join(sconfig['paths']['logs'], '_error.log')),
            }
        )

        if sconfig['daemon']:
            cherrypy.process.plugins.Daemonizer(self.bus).subscribe()

        self.bus.subscribe('stop', self.remove_all_sloths)

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
            ExtendedSloth, errors = Sloth.extend(config.get('extensions'))

            sloth = ExtendedSloth(config)

            for error in errors:
                sloth.logger.error(error)

            listen_to = sloth.listen_to

            if listen_to in self.listen_points:
                raise ValueError('Listen point %s is already taken' % listen_to)

            self.config_files[config_source] = sloth

            self.listen_points[listen_to] = sloth
            sloth.logger.info('Listening on %s' % listen_to)

        except Exception as e:
            cherrypy.log.error(
                'Could not add Sloth app from the config source %s: %s' % (config_source, e),
                severity=logging.ERROR
            )

    def update_sloth(self, config_file):
        '''Update Sloth app config when the config file changes.

        Instead of just updating the config in the Sloth app, we remove the app and create it anew.

        This is done to guarantee that the new extensions are loaded and the listen point is updated.

        :param config_file: Sloth app config file
        '''

        self.remove_sloth(config_file)
        self.add_sloth(config_file)

    def remove_sloth(self, listen_point):
        '''Stop Sloth app and remove it from the bed.

        :param config_file: Sloth app config file
        '''

        self.listen_points.pop(listen_point).stop()

    def remove_all_sloths(self):
        '''Stop all active Sloth apps and remove them from the bed.'''

        while self.config_files:
            sloth = self.config_files.popitem()[1]

            self.listen_points.pop(sloth.listen_to)

            sloth.stop()

    @cherrypy.expose
    @cherrypy.tools.proxy()
    def listener(self, listen_to, **kwargs):
        '''Listens for payloads and routes them to the responsible Sloth app.

        :param listen_to: Sloth app listen point (part of the URL after the server host)
        '''

        sloth = self.listen_points.get(listen_to)

        if sloth:
            sloth.handle(cherrypy.request)

        else:
            raise cherrypy.HTTPError(404, 'This listen point does not exist.')