'''Sloth CI.

Usage:
  sloth-ci start | restart | stop [-c <file>]
  sloth-ci create <config_source> [-c <file>]
  sloth-ci remove <listen_point> [-c <file>]
  sloth-ci trigger <listen_point> [-p <params>] [-c <file>]
  sloth-ci --version
  sloth-ci -h

Options:
  -c <file>, --config <file>    Path to the server config file [default: ./sloth.yml]
  -p --params <params>          Params to trigger the actions with. String like 'param1=val1,param2=val2'
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
            print('Either put a "sloth.yml" file in this directory or pick a proper config file with "-c."')
            exit()

    def start(self):
        try:
            Bed(self.config).start()

        except Exception as e:
            print('Could not start Sloth CI: %s' % e)

    def _send_api_request(self, data):
        response = post(self.api_url, auth=self.api_auth, data=data)

        return response.status_code, response.text.strip()

    def create_app(self, config_source):
        data = {
            'action': 'create',
            'config_source': config_source
        }

        status, text = self._send_api_request(data)
        
        if status == 201:
            print('App created, listening on %s' % text)

        else:
            print('App was not created: %s' % text)

    def remove_app(self, listen_point):
        data = {
            'action': 'remove',
            'listen_point': listen_point
        }

        status, text = self._send_api_request(data)
        
        if status == 204:
            print('App on listen point %s removed' % listen_point)

        else:
            print('App was not removed: %s' % text)

    def trigger_actions(self, listen_point, param_string):
        params = dict((pair.split('=') for pair in param_string.split(',')))

        data = {
            'action': 'trigger',
            'listen_point': listen_point
        }

        data.update(params)
        
        status, text = self._send_api_request(data)

        if status == 202:
            print('App actions on listen point %s triggered' % listen_point)

        else:
            print('App actions were not triggered: %s' % text)

    def restart(self):
        status, text = self._send_api_request({'action': 'restart'})
        
        if status == 202:
            print('Restarting Sloth CI')

        else:
            print('Server was not restarted: %s' % text)

    def stop(self):
        status, text = self._send_api_request({'action': 'stop'})
        
        if status == 202:
            print('Stopping Sloth CI')

        else:
            print('Server was not stopped: %s' % text)


def main():
    args = docopt(__doc__, version=__version__)

    cli = CLI(args['--config'])

    if args['start']:
        cli.start()

    elif args['create']:
        cli.create_app(args['<config_source>'])

    elif args['remove']:
        cli.remove_app(args['<listen_point>'])

    elif args['trigger']:
        cli.trigger_actions(args['<listen_point>'], args['--params'])

    elif args['restart']:
        cli.restart()

    elif args['stop']:
        cli.stop()