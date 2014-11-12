'''Sloth CI.

Usage:
  sloth-ci start [-d] [-c <file>]
  sloth-ci create-app <config_source> [-c <file>]
  sloth-ci remove-app <listen_point> [-c <file>]
  sloth-ci restart [-c <file>]
  sloth-ci stop [-c <file>]
  sloth-ci --version
  sloth-ci -h

Options:
  -d --daemon                   Start as daemon (UNIX only)
  -c <file>, --config <file>    Path to the config file [default: ./sloth.yml]
  -h --help                     Show this screen
  -v --version                  Show version
'''


from sys import exit

from docopt import docopt

from yaml import load
from requests import post

from . import __version__
from .bed import Bed


class CLI:
    def __init__(self, path_to_config_file):
        try:
            self.config = load(open(path_to_config_file))
        
            self.api_url = 'http://%s:%d' % (self.config['host'], self.config['port'])
            self.api_auth = (self.config['api_auth']['login'], self.config['api_auth']['password'])

        except FileNotFoundError:
            print('Either put a "sloth.yml" file in this directory or pick a config file with "-c."')
            exit()

    def start(self):
        try:
            Bed(self.config).start()

        except Exception as e:
            print('Invalid config file.')

    def _send_api_request(self, data):
        return post(self.api_url, auth=self.api_auth, data=data)

    def create_app(self, config_source):
        response = self._send_api_request({'action': 'create-app', 'config_source': config_source})
        
        if response.status_code == 200:
            print('App created, listening on %s' % response.text)

        else:
            print('App was not created: %s' % response.text)

    def remove_app(self, listen_point):
        response = self._send_api_request({'action': 'remove-app', 'listen_point': listen_point})
        
        if response.status_code == 200:
            print('App on listen point %s removed' % response.text)

        else:
            print('App was not removed: %s' % response.reason)

    def restart(self):
        print(self._send_api_request({'action': 'restart'}).text)

    def stop(self):
        print(self._send_api_request({'action': 'stop'}).text)


def main():
    args = docopt(__doc__, version=__version__)

    cli = CLI(args['--config'])

    if args['start']:
        cli.start()

    elif args['create-app']:
        cli.create_app(args['<config_source>'])

    elif args['remove-app']:
        cli.remove_app(args['<listen_point>'])

    elif args['restart']:
        cli.restart()

    elif args['stop']:
        cli.stop()