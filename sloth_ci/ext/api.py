def extend_bed(cls, extension):
    import cherrypy

    from cherrypy.lib.auth_basic import checkpassword_dict

    from yaml import load

    import sqlite3

    from .. import __version__

    class Bed(cls):
        def __init__(self, config):
            super().__init__(config)

            self.actions = {
                'create': self.create,
                'bind': self.bind,
                'remove': self.remove,
                'trigger': self.trigger,
                'info': self.info,
                'list': self.list,
                'logs': self.logs,
                'history': self.history,
                'version': self.version,
                'restart': self.restart,
                'stop': self.stop
            }

        def _setup_routing(self):
            '''Setup routing for the API endpoint.'''

            super()._setup_routing()

            auth = self.config['api_auth']

            listener = self._make_listener({auth['login']: auth['password']})

            self._dispatcher.connect('api', '/', listener)

        def _handle_error(self, status, message, traceback, version):
            return message

        def _make_listener(self, auth_dict, realm='sloth-ci'):
            '''Get a basic-auth-protected listener function for the API endpoint.

            :param auth_dict: {user: password} dict for authentication
            :param realm: mandatory param for basic auth

            :returns: a CherryPy listener function
            '''

            @cherrypy.expose
            @cherrypy.tools.auth_basic(checkpassword=checkpassword_dict(auth_dict), realm=realm)
            @cherrypy.tools.json_out()
            def listener(action, **kwargs):
                '''Listen to and route API requests.

                An API request is an HTTP request with two mandatory parameters: ``action`` and ``params``.

                :param action: string corresponding to one of the available API methods.
                :param params: a single object, a list, or a dict of params for the action.
                '''

                cherrypy.request.error_page = {'default': self._handle_error}

                try:
                    return self.actions[action](kwargs)

                except KeyError as e:
                    raise cherrypy.HTTPError(404, 'Action %s not found' % e)

            return listener

        def bind(self, kwargs):
            '''Bind an app with a config file.'''

            listen_point = kwargs.get('listen_point')
            config_file = kwargs.get('config_file')

            if not listen_point:
                raise cherrypy.HTTPError(400, 'Missing parameter "listen_point"')

            if not config_file:
                raise cherrypy.HTTPError(400, 'Missing parameter config_file')

            try:
                self.bind_to_file(listen_point, config_file)

                cherrypy.response.status = 200

                return None

            except KeyError as e:
                raise cherrypy.HTTPError(404, 'Listen point %s not found' % e)

            except FileNotFoundError as e:
                raise cherrypy.HTTPError(404, 'File %s not found' % e)

            except ValueError:
                raise cherrypy.HTTPError(500, 'Config mismatch')

            except Exception as e:
                raise cherrypy.HTTPError(500, 'Failed to bind config file to app: %s' % e)

        def create(self, kwargs):
            '''Create an app from the given config string.'''

            config_string = kwargs.get('config_string')

            if not config_string:
                raise cherrypy.HTTPError(400, 'Missing parameter config_string')

            try:
                listen_point = self.create_from_config(load(config_string))

                cherrypy.response.status = 201

                return listen_point

            except TypeError:
                raise cherrypy.HTTPError(500, '"%s" is not a valid config string' % config_string)

            except KeyError as e:
                raise cherrypy.HTTPError(500, 'The "%s" param is missing in the config' % e)

            except ValueError as e:
                raise cherrypy.HTTPError(409, 'Listen point %s is taken' % e)

            except Exception as e:
                raise cherrypy.HTTPError(500, 'Failed to create app: %s' % e)

        def history(self, kwargs):
            '''Get paginated app build history from the database.'''

            if not self.db_path:
                raise cherrypy.HTTPError(501, "This Sloth server doesn't have a database to store build history")

            listen_point = kwargs.get('listen_point')

            if not listen_point:
                raise cherrypy.HTTPError(400, 'Missing parameter "listen_point"')

            try:
                if not listen_point in self.sloths:
                    raise KeyError(listen_point)

                from_page = int(kwargs.get('from_page', 1))
                to_page = int(kwargs.get('to_page', from_page))
                per_page = int(kwargs.get('per_page', 10))
                level = int(kwargs.get('level', 20))

                connection = sqlite3.connect(self.db_path)
                cursor = connection.cursor()

                query = 'SELECT * FROM build_history \
                    WHERE logger_name=? \
                    AND level_number >= ? \
                    ORDER BY timestamp DESC \
                    LIMIT ? OFFSET ?'

                query_params = (
                    listen_point + '.build',
                    level,
                    (to_page - from_page + 1) * per_page,
                    (from_page - 1) * per_page
                )

                cursor.execute(query, query_params)

                column_names = [column[0] for column in cursor.description]

                history = [dict(zip(column_names, record)) for record in cursor.fetchall()]

                connection.close()

                cherrypy.response.status = 200

                return history

            except KeyError as e:
                raise cherrypy.HTTPError(404, 'Listen point %s not found' % e)

            except Exception as e:
                raise cherrypy.HTTPError(500, 'Failed to get app build history: %s' % e)

        def info(self, kwargs):
            '''Get information about an app on an given listen point.'''

            listen_point = kwargs.get('listen_point')

            if not listen_point:
                raise cherrypy.HTTPError(400, 'Missing parameter "listen_point"')

            try:
                if not listen_point in self.sloths:
                    raise KeyError(listen_point)

                info = {
                    'config_file': self.config_files.get(listen_point)
                }

                if self.db_path:
                    last_build_info = self.history({
                        'listen_point': listen_point,
                        'per_page': 1
                    })

                    if last_build_info:
                        last_build_status_message = last_build_info[0]['message']
                        last_build_status_level = last_build_info[0]['level_name']
                        last_build_timestamp = last_build_info[0]['timestamp']

                    else:
                        last_build_status_message = 'Never triggered'
                        last_build_status_level = 'Never triggered'
                        last_build_timestamp = 0

                    info['last_build_status_message'] = last_build_status_message
                    info['last_build_status_level'] = last_build_status_level
                    info['last_build_timestamp'] = last_build_timestamp

                else:
                    info['last_build_status_message'] = 'Not available'
                    info['last_build_status_level'] = 'Not available'
                    info['last_build_timestamp'] = 0

                cherrypy.response.status = 200

                return info

            except KeyError as e:
                raise cherrypy.HTTPError(404, 'Listen point %s not found' % e)

            except Exception as e:
                raise cherrypy.HTTPError(500, 'Failed to get app info: %s' % e)

        def list(self, kwargs):
            '''List all available apps.'''

            try:
                app_list = self.sloths.keys()
                
                cherrypy.response.status = 200

                return sorted(app_list)

            except Exception as e:
                raise cherrypy.HTTPError(500, 'Failed to get app list: %s' % e)

        def logs(self, kwargs):
            '''Get paginated app logs from the database.'''

            if not self.db_path:
                raise cherrypy.HTTPError(501, "This Sloth server doesn't have a database to store logs")

            listen_point = kwargs.get('listen_point')

            if not listen_point:
                raise cherrypy.HTTPError(400, 'Missing parameter "listen_point"')

            try:
                if not listen_point in self.sloths:
                    raise KeyError(listen_point)

                from_page = int(kwargs.get('from_page', 1))
                to_page = int(kwargs.get('to_page', from_page))
                per_page = int(kwargs.get('per_page', 10))
                level = int(kwargs.get('level', 20))

                connection = sqlite3.connect(self.db_path)
                cursor = connection.cursor()

                query = 'SELECT * FROM app_logs \
                    WHERE (logger_name=? OR logger_name=? OR logger_name=?) \
                    AND level_number >= ? \
                    ORDER BY timestamp DESC \
                    LIMIT ? OFFSET ?'

                query_params = (
                    listen_point,
                    listen_point + '.exec',
                    listen_point + '.build',
                    level,
                    (to_page - from_page + 1) * per_page,
                    (from_page - 1) * per_page
                )

                cursor.execute(query, query_params)

                column_names = [column[0] for column in cursor.description]

                logs = [dict(zip(column_names, record)) for record in cursor.fetchall()]

                connection.close()

                cherrypy.response.status = 200

                return logs

            except KeyError as e:
                raise cherrypy.HTTPError(404, 'Listen point %s not found' % e)

            except Exception as e:
                raise cherrypy.HTTPError(500, 'Failed to get app logs: %s' % e)

        def remove(self, kwargs):
            '''Remove an app on the given listen point.'''

            listen_point = kwargs.get('listen_point')

            if not listen_point:
                raise cherrypy.HTTPError(400, 'Missing parameter "listen_point"')

            try:
                super().remove(listen_point)

                cherrypy.response.status = 204

                return None

            except KeyError as e:
                raise cherrypy.HTTPError(404, 'Listen point %s not found' % e)

            except Exception as e:
                raise cherrypy.HTTPError(500, 'Failed to remove app: %s' % e)

        def restart(self, kwargs):
            '''Ask the Sloth CI server to restart.'''

            try:
                self.bus.restart()

                cherrypy.response.status = 202

                return None

            except Exception as e:
                raise cherrypy.HTTPError(500, 'Failed to restart Sloth CI server: %s' % e)

        def stop(self, kwargs):
            '''Ask the Sloth CI server to stop.'''

            try:
                self.bus.exit()

                cherrypy.response.status = 202

                return None

            except Exception as e:
                raise cherrypy.HTTPError(500, 'Failed to stop Sloth CI server: %s' % e)

        def trigger(self, kwargs):
            '''Trigger action of an app on the given listen point.'''

            listen_point = kwargs.get('listen_point')

            if not listen_point:
                raise cherrypy.HTTPError(400, 'Missing parameter "listen_point"')

            try:
                params = {key: kwargs[key] for key in kwargs if key not in ('action', 'listen_point')}

                sloth = self.sloths[listen_point]

                sloth.process(params)

                cherrypy.response.status = 202

                return None

            except KeyError as e:
                raise cherrypy.HTTPError(404, 'Listen point %s not found' % e)

            except Exception as e:
                raise cherrypy.HTTPError(500, 'Failed to trigger app actions: %s' % e)

        def version(self, kwargs):
            '''Get the Sloth CI app version.'''

            try:
                version = __version__

                cherrypy.response.status = 200

                return version

            except Exception as e:
                raise cherrypy.HTTPError(500, 'Failed to get Sloth CI server version: %s' % e)


    return Bed


def extend_cli(cls, extension):
    from os.path import abspath
    from glob import glob
    from collections import namedtuple
    from functools import partial
    from time import ctime

    from tabulate import tabulate
    from cliar import add_aliases
    
    from requests import post, exceptions


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


    def colorize(table, based_on_column, hide_level=True):
        '''Colorize logs table according to message status.

        :param table: logs table, each row is [timestamp, message, level_name]
        :param based_on_column: number of column that holds record level names for coloring

        :returns: colorized table
        '''

        colorized_table = []

        from colorama import init, Fore, Back

        init()

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

            if hide_level:
                row.pop(based_on_column)

            colorized_table.append(list(map(lambda cell: color + cell + reset, row)))

        return colorized_table


    class CLI(cls):
        '''API CLI for Sloth CI.'''

        def __init__(self):
            super().__init__()

            api_url = 'http://%s:%d' % (self.config['host'], self.config['port'])
            api_auth = (self.config['api_auth']['login'], self.config['api_auth']['password'])

            self.send_api_request = partial(send_api_request, api_url, api_auth)

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
                        colorize(rows, based_on_column=-1, hide_level=False),
                        headers=headers
                    )

                else:
                    table = tabulate(
                        colorize(rows, based_on_column=-1),
                        headers=headers
                    )

                print(table)

            else:
                print('Failed to get app build history: %s' % response.content)

        def info(self, app):
            '''get information about the APP'''

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
                    colorize(rows, based_on_column=-1),
                    headers=headers
                )

                print(table)

            else:
                print('Failed to get app info: %s' % response.content)

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
                print('Failed to get app list: %s' % response.content)

        @add_aliases(['log', 'lg'])
        def logs(self, app, from_page:int=1, to_page:int=1, per_page:int=10, level:int=20, verbose=False):
            '''get logs for the APP'''
            
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
                        colorize(rows, based_on_column=-1, hide_level=False),
                        headers=headers
                    )

                else:
                    table = tabulate(
                        colorize(rows, based_on_column=-1),
                        headers=headers
                    )

                print(table)

            else:
                print('Failed to get app logs: %s' % response.content)

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
                print('Failed to get app info: %s' % response.content)

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
                print('Failed to remove app: %s' % response.content)

        def restart(self):
            '''restart the server'''

            response = self.send_api_request(
                {
                    'action': 'restart'
                }
            )

            if response.status_code == 202:
                print('Restarting Sloth CI on http://%s:%d' % (self.config['host'], self.config['port']))
            
            else:
                print('Failed to restart Sloth CI: %s' % response.content)

        @add_aliases(['stat'])
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
            '''stop the server'''

            response = self.send_api_request(
                {
                    'action': 'stop'
                }
            )

            if response.status_code == 202:
                print('Stopping Sloth CI on http://%s:%d' % (self.config['host'], self.config['port']))
            
            else:
                print('Failed to stop Sloth CI: %s' % response.content)


        @add_aliases(['run'])
        def trigger(self, app, params=()):
            '''trigger APP's actions with given PARAMS'''

            data = {
                'action': 'trigger',
                'listen_point': app    
            }

            for param in params:
                key, value = param.split('=')
                data[key] = value

            response = self.send_api_request(data)

            if response.status_code == 202:
                print('Actions triggered on %s' % app)

            else:
                print('Failed to trigger actions: %s' % response.content)


    return CLI
