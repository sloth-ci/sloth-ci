from sys import exit
from importlib import import_module

from os.path import abspath, join, exists
from os import makedirs

from argparse import ArgumentParser

import cherrypy

from configs import load

from .utils import ConfigChecker, get_default_configs_path, get_default_logs_path
from .bed import Bed

def run(host, port, log_dir, daemon, config_locations):
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

    if daemon:
        cherrypy.process.plugins.Daemonizer(cherrypy.engine).subscribe()

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
    parser.add_argument('-s', '--sconfig', help='Server config.')
    parser.add_argument('-H', '--host', help='Host for the Sloth server (overrides value in sconfig).')
    parser.add_argument('-p', '--port', type=int, help='Port for the Sloth server (overrides value in sconfig).')
    parser.add_argument('-l', '--log_dir', help='Where the log files should be stored (overrides value in sconfig).')
    parser.add_argument('-d', '--daemon', action='store_true', help='Run as daemon.')
    parser.add_argument('config', nargs='*', help='Sloth app config files or dirs.')

    parsed_args = parser.parse_args()

    sconfig_file = parsed_args.sconfig

    if sconfig_file:
        sconfig = load(sconfig_file)
    else:
        try:
            sconfig = load(join(get_default_configs_path(), 'server.conf'))
        except:
            sconfig = {}

    host = parsed_args.host or sconfig.get('host')
    port = parsed_args.port or sconfig.get('port')
    log_dir = parsed_args.log_dir or sconfig.get('log_dir') or get_default_logs_path()
    daemon = parsed_args.daemon or sconfig.get('daemon')

    if not (host and port and log_dir):
        exit('Missing server param(s).')

    config_locations = parsed_args.config or join(get_default_configs_path(), 'apps')

    if not exists(abspath(log_dir)):
        makedirs(abspath(log_dir))

    run(host, port, log_dir, daemon, config_locations)