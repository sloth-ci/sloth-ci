'''Sloth CI.

Usage:
  sloth-ci (start | restart | stop) [-c <file>]
  sloth-ci create <config_files>... [-c <file>]
  sloth-ci remove <listen_points>... [-c <file>]
  sloth-ci trigger <listen_point> [-p <params>] [-c <file>]
  sloth-ci (info | reload) [<listen_points>...] [-c <file>]
  sloth-ci --status
  sloth-ci --version
  sloth-ci --help

Options:
  -c <file>, --config <file>    Path to the server config file [default: ./sloth.yml]
  -p --params <params>          Params to trigger the actions with. String like 'param1=val1,param2=val2'
  -s --status                   Show server status (running/not running)
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

    def start(self):
        '''Start a Sloth CI server.'''

        try:
            print('Starting Sloth CI on %s' % self.api_url)
            Bed(self.config).start()

        except Exception as e:
            print('Could not start Sloth CI: %s' % e)

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
        
        except exceptions.ConnectionError as e:
            print('Failed to connect to Sloth CI on %s' % self.api_url)
            exit()

    def _bind_config_file(self, listen_point, config_file):
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
            print('App on %s bound with file %s' % (listen_point, config_file))

        else:
            print('App and file were not bound: %s' % content)

    def create_apps(self, config_files):
        '''Create apps from the config files.
        
        :param config_files: paths to the app config files
        '''

        for config_file in config_files:
            try:
                config_file_abspath = abspath(config_file)

                data = {
                    'action': 'create',
                    'config_string': ''.join(open(config_file_abspath).readlines()),
                }

                status, content = self._send_api_request(data)

                if status == 201:
                    print('App created, listening on %s' % content)

                    self._bind_config_file(content, config_file_abspath)

                else:
                    print('App was not created: %s' % content)
        
            except FileNotFoundError as e:
                print('File %s not found' % e)

    def remove_apps(self, listen_points):
        '''Remove apps on certain listen points.
        
        :param listen_points: list of listen points
        '''

        for listen_point in listen_points:
            data = {
                'action': 'remove',
                'listen_point': listen_point
            }

            status, content = self._send_api_request(data)
        
            if status == 204:
                print('App on listen point %s removed' % listen_point)

            else:
                print('App was not removed: %s' % content)

    def trigger_actions(self, listen_point, param_string):
        '''Trigger actions of a particular app to execute with the given params.

        :param listen_point: app's listen point
        :param param_string: string like "param1=value1,param2=value2"
        '''
        
        if param_string:
            params = dict((pair.split('=') for pair in param_string.split(',')))
        
        else:
            params = {}

        data = {
            'action': 'trigger',
            'listen_point': listen_point
        }

        data.update(params)
        
        status, content = self._send_api_request(data)

        if status == 202:
            print('App actions on listen point %s triggered' % listen_point)

        else:
            print('App actions were not triggered: %s' % content)

    def app_info(self, listen_points=[]):
        '''Get info for a particular app or all apps.
 
        :param listen_points: list of app listen points to show info for; if empty, all apps will be shown
        
        :returns: list of dicts with keys listen_point and config_file
        '''

        data = {
            'action': 'info',
            'listen_point': listen_points
        }

        status, content = self._send_api_request(data)

        if status == 200:
            return content

        elif status == 404:
            raise KeyError(content)

        else:
            raise RuntimeError(content)

    def reload_apps(self, listen_points):
        '''Reload a particluar app or all apps.
        
        :param listen_points: list of listen points of apps to be reloaded; if empty, all apps will be realoaded
        '''

        if not listen_points:
            reload_list = [app['listen_point'] for app in self.app_info()]

        else:
            reload_list = listen_points

        for listen_point in reload_list:
            try:
                config_file = self.app_info([listen_point])[0]['config_file']

                self.remove_apps([listen_point])
                self.create_apps([config_file])

            except Exception as e:
                print('App was not reloaded: %s' % e)

    def get_status(self):
        try:
            self._send_api_request()
            print('Sloth CI is running on %s' % self.api_url)

        except:
            print('Sloth CI is not running on %s' % self.api_url)

    def restart(self):
        '''Restart a Sloth CI server.'''

        status, content = self._send_api_request({'action': 'restart'})
        
        if status == 202:
            print('Restarting Sloth CI')

        else:
            print('Server was not restarted: %s' % content)

    def stop(self):
        '''Stop a Sloth CI server.'''

        status, content = self._send_api_request({'action': 'stop'})
        
        if status == 202:
            print('Stopping Sloth CI')

        else:
            print('Server was not stopped: %s' % content)


def main():
    args = docopt(__doc__, version=__version__)

    cli = CLI(args['--config'])

    if args['start']:
        cli.start()

    elif args['create']:
        cli.create_apps(args['<config_files>'])

    elif args['remove']:
        cli.remove_apps(args['<listen_points>'])

    elif args['trigger']:
        cli.trigger_actions(args['<listen_point>'], args['--params'])

    elif args['info']:
        try:
            print(tabulate(
                cli.app_info(args['<listen_points>']) or {},
                headers='keys'
            ))

        except Exception as e:
            print('Failed to get app info: %s' % e)

    elif args['reload']:
        cli.reload_apps(args['<listen_points>'])

    elif args['--status']:
        cli.get_status()

    elif args['restart']:
        cli.restart()

    elif args['stop']:
        cli.stop()