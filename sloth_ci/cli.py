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


from docopt import docopt

from yaml import load
from requests import post

from . import __version__
from .bed import Bed


class CLI:
    def __init__(self, path_to_config_file):
        self.sconfig = load(open(path_to_config_file))

        self.api_url = 'http://%s:%d' % (self.sconfig['host'], self.sconfig['port'])
        self.api_auth = (self.sconfig['api_auth']['login'], self.sconfig['api_auth']['password'])

    def start(self):
        try:
            Bed(self.sconfig).start()

        except FileNotFoundError:
            print('Either put a sloth.yml file in this directory or specify the path with -c.')

        except Exception as e:
            print('Invalid config file.')

    def _send_api_request(self, data):
        return post(self.api_url, auth=self.api_auth, data=data).content

    def create_app(self, config_source):
        print(self._send_api_request({'action': 'create-app', 'config_source': config_source}))

    def remove_app(self, listen_point):
        print(self._send_api_request({'action': 'remove-app', 'listen_point': listen_point}))

    def restart(self):
        print(self._send_api_request({'action': 'restart'}))

    def stop(self):
        print(self._send_api_request({'action': 'stop'}))


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