def extend_cli(cls, extension):
    '''Add command-line commands for the API interaction.

    :param cls: base :class:`CLI <sloth_ci.cli.CLI>` class to be extended
    :param extension: ``{'api': {'module': 'api'}}``

    :returns: extended :class:`CLI <sloth_ci.cli.CLI>` class
    '''

    from sys import exit
    from os.path import abspath
    from glob import glob
    from collections import namedtuple
    from functools import partial
    from time import ctime

    from tabulate import tabulate
    from cliar import add_aliases

    from requests import post, exceptions


    class CLI(cls):
        '''Welcome to Sloth CI API CLI!

Run "sci start" to start the server.

Run "sci -h" to see all available commands.

Run "sci <command> -h" to get help for a specific command.
'''

        def __init__(self):
            super().__init__()

            api_url = 'http://%s:%d' % (self.config['host'], self.config['port'])

            for alias in ('auth', 'api_auth'):
                auth = self.config.get(alias)
                if auth:
                    try:
                        api_auth = (auth[0]['login'], auth[0]['password'])

                    except KeyError:
                        api_auth = (auth['login'], auth['password'])

                    finally:
                        break
            else:
                api_auth = None

            self.send_api_request = partial(self.send_api_request, api_url, api_auth)

        @staticmethod
        def send_api_request(url, auth, data={}):
            '''Send a POST request to a Sloth CI API server with the given data.

            :param url: URL of the Sloth CI API server
            :param auth: login and password to access the Sloth CI API
            :param data: dict of data to be sent with the request
            '''

            APIResponse = namedtuple('APIResponse', ('status_code', 'content'))

            try:
                response = post(url, auth=auth, data=data)

                if response.ok:
                    if response.content:
                        content = response.json()

                    else:
                        content = None

                else:
                    content = response.text.strip()

                return APIResponse(response.status_code, content)

            except exceptions.ConnectionError:
                return APIResponse(503, 'Failed to connect to Sloth CI on %s' % url)

        @staticmethod
        def colorize(table, based_on_column, hide_level=True):
            '''Colorize logs table according to message status.

            :param table: logs table, each row is [timestamp, message, level_name]
            :param based_on_column: number of column that holds record level names for coloring

            :returns: colorized table
            '''
            try:
                from colorama import init, Fore, Back

                init()
                colorized_table = []

            except ImportError:
                colorized_table = table

            if not colorized_table:
                for row in table:
                    reset = Fore.RESET + Back.RESET

                    level_name = row[based_on_column]

                    if level_name == 'DEBUG':
                        color = Fore.CYAN
                    elif level_name == 'INFO':
                        color = Fore.GREEN
                    elif level_name == 'WARNING':
                        color = Fore.YELLOW
                    elif level_name == 'ERROR':
                        color = Fore.RED
                    elif level_name == 'CRITICAL':
                        color = Fore.RED + Back.WHITE
                    else:
                        color = reset

                    colorized_row = [(color + cell + reset) for cell in row]
                    colorized_table.append(colorized_row)

            if hide_level:
                for row in colorized_table:
                    row.pop(based_on_column)

            return colorized_table


        @add_aliases(['add'])
        def create(self, paths:tuple):
            '''create apps from PATHS and bind them with respective configs'''

            for path in paths:
                config_files = glob(path)

                if not config_files:
                    print('Path %s not found' % path)
                    continue

                for config_file in config_files:
                    response = self.send_api_request(
                        {
                            'action': 'create',
                            'config_string': open(config_file).read()
                        }
                    )

                    if response.status_code == 201:
                        listen_point = response.content
                        print('App "%s" created' % listen_point)

                    else:
                        print('Failed to create app: %s' % response.content)
                        continue

                    response = self.send_api_request(
                        {
                            'action': 'bind',
                            'listen_point': listen_point,
                            'config_file': abspath(config_file)
                        }
                    )

                    if response.status_code == 200:
                        print('App "%s" bound with config file "%s"' % (listen_point, config_file))

                    else:
                        print('Failed to bind app with config file: %s' % response.content)

        @add_aliases(['hist', 'builds'])
        def history(self, app, from_page:int=1, to_page:int=1, per_page:int=10, level:int=20, verbose=False):
            '''get build history for APP'''

            response = self.send_api_request(
                {
                    'action': 'history',
                    'listen_point': app,
                    'from_page': from_page,
                    'to_page': to_page,
                    'per_page': per_page,
                    'level': level
                }
            )

            if response.status_code == 200:
                rows = [
                    [
                        ctime(record['timestamp']),
                        record['message'],
                        record['level_name']
                    ] for record in response.content
                ]

                headers = [
                    'Timestamp',
                    'Status',
                    'Level'
                ]

                if verbose:
                    table = tabulate(
                        self.colorize(rows, based_on_column=-1, hide_level=False),
                        headers=headers
                    )

                else:
                    table = tabulate(
                        self.colorize(rows, based_on_column=-1),
                        headers=headers
                    )

                print(table)

            else:
                exit('Failed to get app build history: %s' % response.content)

        def info(self, app):
            '''get information about APP'''

            response = self.send_api_request(
                {
                    'action': 'info',
                    'listen_point': app
                }
            )

            if response.status_code == 200:
                info = response.content

                rows = [[
                    info['config_file'],
                    info['last_build_status_message'],
                    ctime(info['last_build_timestamp']),
                    info['last_build_status_level']
                ]]

                headers = [
                    'Config File',
                    'Last Build Message',
                    'Last Build Timestamp'
                ]

                table = tabulate(
                    self.colorize(rows, based_on_column=-1),
                    headers=headers
                )

                print(table)

            else:
                exit('Failed to get app info: %s' % response.content)

        @add_aliases(['ls'])
        def list(self):
            '''list all available apps'''

            response = self.send_api_request(
                {
                    'action': 'list'
                }
            )

            if response.status_code == 200:
                for app in response.content:
                    print(app)

            else:
                exit('Failed to get app list: %s' % response.content)

        @add_aliases(['lg'])
        def logs(self, app, from_page:int=1, to_page:int=1, per_page:int=10, level:int=20, verbose=False):
            '''get logs for APP'''

            response = self.send_api_request(
                {
                    'action': 'logs',
                    'listen_point': app,
                    'from_page': from_page,
                    'to_page': to_page,
                    'per_page': per_page,
                    'level': level
                }
            )

            if response.status_code == 200:
                rows = [
                    [
                        ctime(record['timestamp']),
                        record['message'],
                        record['level_name']
                    ] for record in response.content
                ]

                headers = [
                    'Timestamp',
                    'Message',
                    'Level'
                ]

                if verbose:
                    table = tabulate(
                        self.colorize(rows, based_on_column=-1, hide_level=False),
                        headers=headers
                    )

                else:
                    table = tabulate(
                        self.colorize(rows, based_on_column=-1),
                        headers=headers
                    )

                print(table)

            else:
                exit('Failed to get app logs: %s' % response.content)

        @add_aliases(['update', 'up'])
        def reload(self, app):
            '''recreate APP to apply config changes'''

            response = self.send_api_request(
                {
                    'action': 'info',
                    'listen_point': app
                }
            )

            if response.status_code == 200:
                self.remove(app)
                self.create([response.content['config_file']])

            else:
                exit('Failed to get app info: %s' % response.content)

        @add_aliases(['del', 'rm'])
        def remove(self, app):
            '''remove APP'''

            response = self.send_api_request(
                {
                    'action': 'remove',
                    'listen_point': app
                }
            )

            if response.status_code == 204:
                print('App "%s" removed' % app)

            else:
                exit('Failed to remove app: %s' % response.content)

        def restart(self):
            '''restart server'''

            response = self.send_api_request(
                {
                    'action': 'restart'
                }
            )

            if response.status_code == 202:
                print('Restarting Sloth CI on http://%s:%d' % (self.config['host'], self.config['port']))

            else:
                exit('Failed to restart Sloth CI: %s' % response.content)

        @add_aliases(['stat', 'st'])
        def status(self):
            '''check server status'''

            response = self.send_api_request(
                {
                    'action': 'version'
                }
            )

            if response.status_code == 200:
                print(
                    'Sloth CI version %s is running on http://%s:%d'
                     % (response.content, self.config['host'], self.config['port'])
                )

            else:
                print('Sloth CI is not running on http://%s:%d' % (self.config['host'], self.config['port']))

        def stop(self):
            '''stop server'''

            response = self.send_api_request(
                {
                    'action': 'stop'
                }
            )

            if response.status_code == 202:
                print('Stopping Sloth CI on http://%s:%d' % (self.config['host'], self.config['port']))

            else:
                exit('Failed to stop Sloth CI: %s' % response.content)


        @add_aliases(['run', 'fire'])
        def trigger(self, app, wait=False, params=()):
            '''trigger APP's actions with given PARAMS

PARAMS are specified as "param1=value1 param2=value ..."
'''

            data = {
                'action': 'trigger',
                'listen_point': app,
                'wait': wait or ''
            }

            for param in params:
                key, value = param.split('=')
                data[key] = value

            response = self.send_api_request(data)

            if response.status_code == 202:
                print('Actions triggered on %s' % app)

            elif response.status_code == 200:
                print(response.content)

            else:
                exit('Failed to trigger actions: %s' % response.content)


    return CLI
