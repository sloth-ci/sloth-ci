'''Sloth CI.

Usage:
  sloth-ci (start | restart | stop | status) [-c <file>]
  sloth-ci create <config_files>... [-c <file>]
  sloth-ci remove <listen_points>... [-c <file>]
  sloth-ci trigger <listen_point> [-p <params>] [-c <file>]
  sloth-ci (info | reload) [<listen_points>...] [-c <file>]
  sloth-ci --version
  sloth-ci --help

Options:
  -c <file>, --config <file>    Path to the server config file [default: ./sloth.yml]
  -p --params <params>          Params to trigger the actions with. String like 'param1=val1,param2=val2'
  -v --version                  Show version
  -h --help                     Show this screen
'''


from sys import exit

from os.path import abspath

from docopt import docopt
from tabulate import tabulate

from yaml import load
from requests import post, exceptions

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

    def _send_api_request(self, data={}):
        '''Send a POST request to the Sloth CI API with the given data.'''

        try:
            response = post(self.api_url, auth=self.api_auth, data=data)

            if response.ok:
                if response.content:
                    content = response.json()

                else:
                    content = None

            else:
                content = response.text.strip()

            return response.status_code, content
        
        except exceptions.ConnectionError:
            raise ConnectionError('Failed to connect to Sloth CI on %s' % self.api_url)

    def bind(self, listen_point, config_file):
        '''Bind a Sloth app with a config file.
 
        :param listen_point: app's listen point
        :param config_file: absolute path to the config file
        '''
        
        data = {
            'action': 'bind',
            'listen_point': listen_point,
            'config_file': config_file
        }
        
        status, content = self._send_api_request(data)

        if status == 200:
            return True

        elif status == 404:
            raise KeyError(content)

        else:
            raise RuntimeError(content)

    def create(self, config_file):
        '''Create an app from the config file.
        
        :param config_file: path to the app config file
        '''

        data = {
            'action': 'create',
            'config_string': ''.join(open(config_file).readlines()),
        }

        status, content = self._send_api_request(data)

        if status == 201:
            return content

        elif status == 409:
            raise ValueError(content)
            
        else:
            raise RuntimeError(content)

    def remove(self, listen_point):
        '''Remove an app on a certain listen point.
        
        :param listen_point: the app's listen point
        '''

        data = {
            'action': 'remove',
            'listen_point': listen_point
        }

        status, content = self._send_api_request(data)
        
        if status == 204:
            return True

        elif status == 404:
            raise KeyError(content)

        else:
            raise RuntimeError(content)

    def trigger(self, listen_point, params={}):
        '''Trigger actions of a particular app to execute with the given params.

        :param listen_point: app's listen point
        :param params: dict of params
        '''

        data = {
            'action': 'trigger',
            'listen_point': listen_point,
        }

        data.update(params)
        
        status, content = self._send_api_request(data)

        if status == 202:
            return True

        elif status == 404:
            raise KeyError(content)

        else:
            raise RuntimeError(content)

    def info(self, listen_points=[]):
        '''Get info for a particular app or all apps.
 
        :param listen_points: list of app listen points to show info for; if empty, all apps will be shown
        
        :returns: list of dicts with keys listen_point and config_file
        '''

        data = {
            'action': 'info',
            'listen_points': listen_points
        }

        status, content = self._send_api_request(data)

        if status == 200:
            return content

        elif status == 404:
            raise KeyError(content)

        else:
            raise RuntimeError(content)

    def restart(self):
        '''Ask a a Sloth CI server to restart.'''

        status, content = self._send_api_request({'action': 'restart'})
        
        if status == 202:
            return True

        else:
            raise RuntimeError(content)

    def stop(self):
        '''Ask a a Sloth CI server to stop.'''

        status, content = self._send_api_request({'action': 'stop'})
        
        if status == 202:
            return True

        else:
            raise RuntimeError(content)


def main():
    args = docopt(__doc__, version=__version__)

    cli = CLI(args['--config'])

    if args['start']:
        try:
            print('Starting Sloth CI on %s' % cli.api_url)
            Bed(cli.config).start()

        except Exception as e:
            print('Failed to start Sloth CI: %s' % e)

    elif args['create']:
        for config_file in args['<config_files>']:
            try:
                listen_point = cli.create(abspath(config_file))
                print('App created on %s' % listen_point)

            except FileNotFoundError:
                print('File %s not found' % config_file)
                continue

            except Exception as e:
                print('Failed to create app: %s' % e)
                continue

            try:
                cli.bind(listen_point, abspath(config_file))
                print('App on %s bound with config file %s' % (listen_point, config_file))

            except Exception as e:
                print('Failed to bind app on %s with config file %s: %s' % (listen_point, config_file, e))

    elif args['remove']:
        for listen_point in args['<listen_points>']:
            try:
                cli.remove(listen_point)
                print('App on %s removed' % listen_point)

            except Exception as e:
                print('Failed to remove app on %s: %s' % (listen_point, e))

    elif args['trigger']:

        try:
            listen_point = args['<listen_point>']
            params = {}

            if args['--params']:
                params.update(dict((pair.split('=') for pair in args['--params'].split(','))))

            cli.trigger(listen_point, params)
            print('Actions triggered on %s' % listen_point)

        except Exception as e:
            print('Failed to trigger actions on %s: %s' % (listen_point, e))

    elif args['info']:
        try:
            apps = cli.info(args['<listen_points>'])
            
            table = [[app['listen_point'], app['config_file']] for app in apps]
            
            print(tabulate(table, headers=['Listen Point', 'Config File']))

        except Exception as e:
            print('Failed to get app info: %s' % e)

    elif args['reload']:
        reload_list = args['<listen_points>'] or [app['listen_point'] for app in cli.info()]

        for listen_point in reload_list:
            try:
                config_file = cli.info([listen_point])[0]['config_file']
                
                cli.remove(listen_point)
                cli.create(config_file)
                cli.bind(listen_point, config_file)

                print('App on %s reloaded' % listen_point)

            except Exception as e:
                print('Failed to reload app on %s: %s' % (listen_point, e))

    elif args['restart']:
        try:
            cli.restart()
            print('Restarting Sloth CI on %s ' % cli.api_url)

        except Exception as e:
            print('Failed to restart Sloth CI on %s: %s' % (cli.api_url, e))

    elif args['stop']:
        try:
            cli.stop()
            print('Stopping Sloth CI on %s ' % cli.api_url)

        except Exception as e:
            print('Failed to stop Sloth CI on %s: %s' % (cli.api_url, e))

    elif args['status']:
        try:
            cli._send_api_request()
            print('Sloth CI is running on %s' % cli.api_url)

        except:
            print('Sloth CI is not running on %s' % cli.api_url)
