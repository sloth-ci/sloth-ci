from importlib import import_module

import cherrypy

from configs import load

from .sloth import Sloth


class Bed:
    '''A container for Sloth apps.

    It tracks their config files and listen points, as well as handles app adding, removing and updating.

    If also implements the listen function for the main CherryPy app.

    (You may wonder, why would I call a module "bed"? Well, that's because a group of sloth is *actually* called "bed". Go ahead, check it on the Internet.)
    '''

    def __init__(self, bus):
        self.config_files = {}
        self.listen_points = {}

        self.bus = bus

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
            self.bus.log('Could not add Sloth app config %s: %s' % (config_file, e), level=40)

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

    def make_listener(self):
        '''Makes a listener function for a particular bed of sloths.'''

        @cherrypy.expose
        @cherrypy.tools.proxy()
        def listener(*path, **kwargs):
            '''Listens for payloads and routes them to the responsible Sloth app.
    
            :param app_name: Sloth app listen point (part of the URL after /) 
            '''

            listen_to = '/'.join(path)

            sloth = self.listen_points.get(listen_to)

            if sloth:
                sloth.logger.debug('Payload received from %s - %s' % (cherrypy.request.remote.ip, cherrypy.request.headers['User-Agent']))

                try:
                    validator = import_module(
                        '.validators.%s' % sloth.config['provider'],
                        package=__package__
                    )
                except ImportError as e:
                    sloth.logger.critical('No matching validator found: %s' % e)
                    raise cherrypy.HTTPError(500, 'No matching validator found: %s' % e)

                validation_data = sloth.config.get('provider_data') or {}

                validation_status, validation_message, validator_params = validator.validate(cherrypy.request, validation_data)

                custom_params = sloth.config.get('params')

                if custom_params:
                    custom_params = custom_params.dict_props

                else:
                    custom_params = {}

                custom_params.update(validator_params)

                params = custom_params

                sloth.logger.debug(validation_message.format_map(validator_params))

                if validation_status == 200:
                    sloth.logger.info('Valid payload received')
                
                else:
                    raise cherrypy.HTTPError(validation_status, validation_message.format_map(validator_params))

                sloth.process(params)
            
            else:
                raise cherrypy.HTTPError(404, 'This listen point does not exist.')

        return listener