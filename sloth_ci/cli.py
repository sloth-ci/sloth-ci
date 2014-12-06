'''Sloth CI.

Usage:
  sloth-ci (start | restart | stop | status) [-c <file>]
  sloth-ci create <config_paths>... [-c <file>]
  sloth-ci remove <listen_points>... [-c <file>]
  sloth-ci trigger <listen_point> [-p <params>] [-c <file>]
  sloth-ci (info | reload) [<listen_points>...] [-c <file>]
  sloth-ci logs <listen_point> [--from-page <number>] [--to-page <number>] [--per-page <number>] [--level <number>] [-c <file>]
  sloth-ci --version
  sloth-ci --help

Options:
  -c <file>, --config <file>    Path to the server config file [default: ./sloth.yml]
  -p --params <params>          Params to trigger the actions with. String like 'param1=val1,param2=val2'
  --from-page <number>          The first page of the logging output.
  --to-page <number>            The last page of the logging output.
  --per-page <number>           Number or log records per page.
  --level <number>              Minimal numeric logging level to be included in the output.
  -v --version                  Show version
  -h --help                     Show this screen
'''


from sys import exit

from os.path import abspath
from glob import glob 
from time import localtime, asctime

from docopt import docopt
from tabulate import tabulate
from yaml import load

from . import __version__
from .bed import Bed
from .api.client import API


class CLI:
    def __init__(self, config_file):
        try:
            self.config = load(open(config_file))
            
            self.api = API(self.config)

        except FileNotFoundError:
            print('Either put "sloth.yml" in this directory or pick a config file with "-c."')
            exit()

        except Exception as e:
            print('Failed to parse the config file: %s' % e)
            exit()

        self.actions = {
            'start': self.start,
            'create': self.create,
            'remove': self.remove,
            'trigger': self.trigger,
            'reload': self.reload,
            'status': self.status,
            'info': self.info,
            'logs': self.logs,
            'restart': self.restart,
            'stop': self.stop
        }

    def start(self, args):
        '''Start a Sloth CI server.'''

        try:
            print('Starting Sloth CI on %s' % self.api.url)
            Bed(self.config).start()

        except Exception as e:
            print('Failed to start Sloth CI: %s' % e)

    def create(self, args):
        '''Create apps from config files and bind them with respective files.'''

        for config_path in args['<config_paths>']:
            config_files = glob(config_path)

            if not config_files:
                print('Path %s not found' % config_path)
                continue

            for config_file in config_files:
                try:
                    listen_point = self.api.create(abspath(config_file))
                    print('App created on %s' % listen_point)

                except Exception as e:
                    print('Failed to create app: %s' % e)
                    continue

                try:
                    self.api.bind(listen_point, abspath(config_file))
                    print('App on %s bound with config file %s' % (listen_point, config_file))

                except Exception as e:
                    print('Failed to bind app on %s with config file %s: %s' % (listen_point, config_file, e))

    def remove(self, args):
        '''Remove apps on listen points.'''

        for listen_point in args['<listen_points>']:
            try:
                self.api.remove(listen_point)
                print('App on %s removed' % listen_point)

            except Exception as e:
                print('Failed to remove app on %s: %s' % (listen_point, e))

    def trigger(self, args):
        '''Trigger app actions on a listen point.'''

        try:
            listen_point = args['<listen_point>']
            params = {}

            if args['--params']:
                params.update(dict((pair.split('=') for pair in args['--params'].split(','))))

            self.api.trigger(listen_point, params)
            print('Actions triggered on %s' % listen_point)

        except Exception as e:
            print('Failed to trigger actions on %s: %s' % (listen_point, e))

    def info(self, args):
        '''Get information about certain or all apps.'''

        try:
            apps = self.api.info(args['<listen_points>'])
            
            table = [[app['listen_point'], app['config_file']] for app in apps]
            
            print(tabulate(table, headers=['Listen Point', 'Config File']))

        except Exception as e:
            print('Failed to get app info: %s' % e)

    def logs(self, args):
        '''Get app logs.'''

        try:
            logs = self.api.logs(
                args['<listen_point>'],
                args['--from-page'],
                args['--to-page'],
                args['--per-page'],
                args['--level']
            )

            table = [
                [
                    asctime(localtime(record['timestamp'])),
                    record['message'],
                    record['level_name']
                ] for record in logs
            ]

            print(tabulate(table, headers=['Timestamp', 'Message', 'Level']))

        except Exception as e:
            print('Failed to get app logs: %s' % e)

    def reload(self, args):
        '''Reload certain or all apps. I.e. remove, recreate, and rebind them with the config files.'''

        try:
            app_list = self.api.info()

        except ConnectionError as e:
            print('Failed to reload apps: %s' % e)
            exit()

        reload_list = args['<listen_points>'] or [app['listen_point'] for app in app_list]

        for listen_point in reload_list:
            try:
                config_file = self.api.info([listen_point])[0]['config_file']
                
                self.api.remove(listen_point)
                new_listen_point = self.api.create(config_file)
                self.api.bind(new_listen_point, config_file)

                print('App on %s reloaded' % listen_point)

            except Exception as e:
                print('Failed to reload app on %s: %s' % (listen_point, e))

    def status(self, args):
        '''Get Sloth CI server status (running or not running).'''

        try:
            self.api._send_api_request()
            print('Sloth CI is running on %s' % self.api.url)

        except:
            print('Sloth CI is not running on %s' % self.api.url)

    def restart(self, args):
        '''Ask a Sloth CI server to restart.'''

        try:
            self.api.restart()
            print('Restarting Sloth CI on %s ' % self.api.url)

        except Exception as e:
            print('Failed to restart Sloth CI on %s: %s' % (self.api.url, e))

    def stop(self, args):
        '''Ask a Sloth CI server to stop.'''

        try:
            self.api.stop()
            print('Stopping Sloth CI on %s ' % self.api.url)

        except Exception as e:
            print('Failed to stop Sloth CI on %s: %s' % (self.api.url, e))


def main():
    args = docopt(__doc__, version=__version__)

    cli = CLI(args['--config'])

    action = [key for key, value in args.items() if value == True][0]

    cli.actions[action](args)