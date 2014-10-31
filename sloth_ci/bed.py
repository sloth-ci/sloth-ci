from importlib import import_module
from os.path import abspath, join
import logging

import cherrypy

from configs import load

from .sloth import Sloth
from .utils import ConfigChecker


@cherrypy.tools.auth_basic(realm='sloth', checkpassword=cherrypy.lib.auth_basic.checkpassword_dict({'user': 'password'}))
@cherrypy.expose
def api(**kwargs):
    return kwargs


class Bed:
    '''A container for Sloth apps.

    It tracks their config files and listen points, as well as handles app adding, removing and updating.

    If also implements the listen function for the main CherryPy app.

    (This module is names "bed" because a group of sloth is actually called "bed".)
    '''
    
    def __init__(self, host, port, log_dir, daemon, config_locations):
        '''Configure CherryPy loop to listen for payload.

        :param host: host
        :param port: port
        :param log_dir: directory to store logs (absolute or relative)
        :param config_locations: Sloth app config file locations
        '''

        self.config_files = {}
        self.listen_points = {}

        routes_dispatcher = cherrypy._cpdispatch.RoutesDispatcher()
        routes_dispatcher.connect('api', '/', api)
        routes_dispatcher.connect('apps', '/{listen_to:.+}', self.listener)

        cherrypy.tree.mount(None, config={
            '/': {
                'request.dispatch': routes_dispatcher,
            }
        })

        cherrypy.config.update(
            {
                'environment': 'production',
                'server.socket_host': host,
                'server.socket_port': port,
                'log.access_file': abspath(join(log_dir, '_access.log')),
                'log.error_file': abspath(join(log_dir, '_error.log')),
                'request.dispatch': routes_dispatcher
            }
        )

        if daemon:
            cherrypy.process.plugins.Daemonizer(cherrypy.engine).subscribe()

        ConfigChecker(cherrypy.engine, config_locations).subscribe()

        cherrypy.engine.subscribe('sloth-add', self.add_sloth)
        cherrypy.engine.subscribe('sloth-update', self.update_sloth)
        cherrypy.engine.subscribe('sloth-remove', self.remove_sloth)
    
        cherrypy.engine.subscribe('stop', self.remove_all_sloths)

    def start(self):
        '''Start CherryPy loop to listen for payload.'''

        cherrypy.engine.start()
        cherrypy.engine.block()

    def add_sloth(self, config_file):
        '''Create a Sloth app from a config file and app it to the bed.
    
        :param config_file: Sloth app config file
        '''

        try:
            config = load(config_file)

            ExtendedSloth, errors = Sloth.extend(config.get('extensions'))

            sloth = ExtendedSloth(config)

            for error in errors:
                sloth.logger.error(error)

            listen_to = sloth.listen_to
            
            if listen_to in self.listen_points:
                raise ValueError('Listen point %s is already taken' % listen_to)         

            self.config_files[config_file] = sloth

            self.listen_points[listen_to] = sloth
            sloth.logger.info('Listening on %s' % listen_to)

        except Exception as e:
            cherrypy.log.error(
                'Could not add Sloth app config %s: %s' % (config_file, e),
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

    def remove_sloth(self, config_file):
        '''Stop Sloth app and remove it from the bed.
    
        :param config_file: Sloth app config file
        '''

        if config_file in self.config_files:
            sloth = self.config_files[config_file]

            self.listen_points.pop(sloth.listen_to)
    
            self.config_files.pop(config_file)
        
            sloth.stop()

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