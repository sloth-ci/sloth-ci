from sys import exit

from os.path import abspath, join, exists
from os import makedirs

from argparse import ArgumentParser

import cherrypy
from configs import load

from .sloth import Sloth
from .utils import ConfigChecker


SLOTHS = {}
LISTENERS = {}


def add_sloth(config_file):
    '''Create a Sloth app from a config file and app it to the Sloth app list.
    
    :param config_file: Sloth app config file
    '''

    try:
        config = load(config_file)

        ExtendedSloth, errors = Sloth.extend(config.get('extensions'))

        sloth = ExtendedSloth(config)

        for error in errors:
            sloth.logger.error(error)

        sloth.logger.debug('Loaded extensions: %s' % ', '.join(sloth.extensions))

        SLOTHS[config_file] = sloth

        sloth.start()
        sloth.logger.info('--- Queue processor started ---')

        listen_to = sloth.config['listen_to']

        LISTENERS[listen_to] = sloth
        sloth.logger.info('Listening on %s' % listen_to)


    except Exception as e:
        cherrypy.log.error('Could not load Sloth app config %s: %s' % (config_file, e))


def update_sloth(config_file):
    '''Update Sloth app config when the config file changes.
    
    :param config_file: Sloth app config file
    '''

    remove_sloth(config_file)
    add_sloth(config_file)


def remove_sloth(config_file):
    '''Stop Sloth app and remove it from the Sloth app list.
    
    :param config_file: Sloth app config file
    '''

    LISTENERS.pop(SLOTHS[config_file].config['listen_to'])
    
    SLOTHS[config_file].stop()

    SLOTHS.pop(config_file)


def remove_all_sloths():
    '''Stop all active Sloth apps.'''
    
    while SLOTHS:
        sloth = SLOTHS.popitem()[1]

        LISTENERS.pop(sloth.config['listen_to'])

        sloth.stop()


@cherrypy.expose
def listen(listen_to, *args, **kwargs):
    '''Listens for payload to a particular Sloth app.
    
    :param app_name: Sloth app name (part of the URL after /) 
    '''

    sloth = LISTENERS.get(listen_to)

    if sloth:
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


def run(host, port, log_dir, config_locations):
    '''Runs CherryPy loop to listen for payload.

    :param host: host
    :param port: port
    :param log_dir: directory to store logs (absolute or relative)
    :param config_files: Sloth app config files
    :param config_dirs: directories to look for Sloth app config files in
    '''

    cherrypy.config.update(
        {
            'environment': 'production',
            'server.socket_host': host,
            'server.socket_port': port,
            'log.access_file': abspath(join(log_dir, '_access.log')),
            'log.error_file': abspath(join(log_dir, '_error.log'))
        }
    )

    ConfigChecker(cherrypy.engine, config_locations).subscribe()

    cherrypy.engine.subscribe('sloth-add', add_sloth)
    cherrypy.engine.subscribe('sloth-update', update_sloth)
    cherrypy.engine.subscribe('sloth-remove', remove_sloth)

    cherrypy.engine.subscribe('stop', remove_all_sloths)

    cherrypy.quickstart(listen)


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

    if not exists(abspath(log_dir)):
        makedirs(abspath(log_dir))

    run(host, port, log_dir, config_locations)