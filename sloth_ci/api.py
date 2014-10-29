from sys import exit

from os.path import abspath, join, exists
from os import makedirs

from argparse import ArgumentParser

import cherrypy

from configs import load

from .utils import get_default_configs_path, get_default_logs_path
from .bed import Bed

def cli():
    '''CLI API function.'''

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

    config_locations = parsed_args.config or join(get_default_configs_path(), 'apps'),

    if not exists(abspath(log_dir)):
        makedirs(abspath(log_dir))

    Bed(host, port, log_dir, daemon, config_locations).start()