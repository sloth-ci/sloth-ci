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


from os.path import abspath

from docopt import docopt
from tabulate import tabulate

from . import __version__
from .bed import Bed
from .api.client import API


def main():
    args = docopt(__doc__, version=__version__)

    try:
        api_client = API(args['--config'])

    except FileNotFoundError:
        print('Either put "sloth.yml" in this directory or pick a config file with "-c."')

    except Exception as e:
        print('Failed to parse the config file: %s' % e)


    if args['start']:
        try:
            print('Starting Sloth CI on %s' % api_client.api_url)
            Bed(api_client.config).start()

        except Exception as e:
            print('Failed to start Sloth CI: %s' % e)

    elif args['create']:
        for config_file in args['<config_files>']:
            try:
                listen_point = api_client.create(abspath(config_file))
                print('App created on %s' % listen_point)

            except FileNotFoundError:
                print('File %s not found' % config_file)
                continue

            except Exception as e:
                print('Failed to create app: %s' % e)
                continue

            try:
                api_client.bind(listen_point, abspath(config_file))
                print('App on %s bound with config file %s' % (listen_point, config_file))

            except Exception as e:
                print('Failed to bind app on %s with config file %s: %s' % (listen_point, config_file, e))

    elif args['remove']:
        for listen_point in args['<listen_points>']:
            try:
                api_client.remove(listen_point)
                print('App on %s removed' % listen_point)

            except Exception as e:
                print('Failed to remove app on %s: %s' % (listen_point, e))

    elif args['trigger']:

        try:
            listen_point = args['<listen_point>']
            params = {}

            if args['--params']:
                params.update(dict((pair.split('=') for pair in args['--params'].split(','))))

            api_client.trigger(listen_point, params)
            print('Actions triggered on %s' % listen_point)

        except Exception as e:
            print('Failed to trigger actions on %s: %s' % (listen_point, e))

    elif args['info']:
        try:
            apps = api_client.info(args['<listen_points>'])
            
            table = [[app['listen_point'], app['config_file']] for app in apps]
            
            print(tabulate(table, headers=['Listen Point', 'Config File']))

        except Exception as e:
            print('Failed to get app info: %s' % e)

    elif args['reload']:
        reload_list = args['<listen_points>'] or [app['listen_point'] for app in api_client.info()]

        for listen_point in reload_list:
            try:
                config_file = api_client.info([listen_point])[0]['config_file']
                
                api_client.remove(listen_point)
                api_client.create(config_file)
                api_client.bind(listen_point, config_file)

                print('App on %s reloaded' % listen_point)

            except Exception as e:
                print('Failed to reload app on %s: %s' % (listen_point, e))

    elif args['restart']:
        try:
            api_client.restart()
            print('Restarting Sloth CI on %s ' % api_client.api_url)

        except Exception as e:
            print('Failed to restart Sloth CI on %s: %s' % (api_client.api_url, e))

    elif args['stop']:
        try:
            api_client.stop()
            print('Stopping Sloth CI on %s ' % api_client.api_url)

        except Exception as e:
            print('Failed to stop Sloth CI on %s: %s' % (api_client.api_url, e))

    elif args['status']:
        try:
            api_client._send_api_request()
            print('Sloth CI is running on %s' % api_client.api_url)

        except:
            print('Sloth CI is not running on %s' % api_client.api_url)
