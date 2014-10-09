from sys import exit
from importlib import import_module

from os.path import abspath, join, exists
from os import makedirs

from argparse import ArgumentParser

import cherrypy

from configs import load

from .utils import ConfigChecker
from .bed import Bed

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

    bed = Bed(cherrypy.engine)

    cherrypy.engine.subscribe('sloth-add', bed.add_sloth)
    cherrypy.engine.subscribe('sloth-update', bed.update_sloth)
    cherrypy.engine.subscribe('sloth-remove', bed.remove_sloth)
    
    cherrypy.engine.subscribe('stop', bed.remove_all_sloths)

    cherrypy.quickstart(bed.make_listener())


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