from cherrypy import expose
from cherrypy import tools
from cherrypy import HTTPError, request, response

from cherrypy.lib.auth_basic import checkpassword_dict

from yaml import load

import sqlite3

from .. import __version__


class API:
    def __init__(self, bed):
        self.bed = bed

        auth = self.bed.config['api_auth']

        self.listener = self._make_listener({auth['login']: auth['password']})

        self.actions = {
            'create': self.create,
            'bind': self.bind,
            'remove': self.remove,
            'trigger': self.trigger,
            'info': self.info,
            'version': self.version,
            'restart': self.restart,
            'stop': self.stop
        }

        if self.bed.db_path:
            self.actions['logs'] = self.logs
            self.actions['history'] = self.history

    def _handle_error(self, status, message, traceback, version):
        return message

    def _make_listener(self, auth_dict, realm='sloth-ci'):
        '''Get a basic-auth-protected listener function for the API endpoint.

        :param auth_dict: {user: password} dict for authentication
        :param realm: mandatory param for basic auth

        :returns: a CherryPy listener function
        '''

        @expose
        @tools.auth_basic(checkpassword=checkpassword_dict(auth_dict), realm=realm)
        @tools.json_out()
        def listener(action, **kwargs):
            '''Listen to and route API requests.

            An API request is an HTTP request with two mandatory parameters: ``action`` and ``params``.

            :param action: string corresponding to one of the available API methods.
            :param params: a single object, a list, or a dict of params for the action.
            '''

            request.error_page = {'default': self._handle_error}

            try:
                return self.actions[action](kwargs)

            except KeyError as e:
                raise HTTPError(404, 'Action %s not found' % action)

        return listener

    def bind(self, kwargs):
        '''Bind an app with a config file.'''

        listen_point = kwargs.get('listen_point')
        config_file = kwargs.get('config_file')

        if not listen_point:
            raise HTTPError(400, 'Missing parameter listen_point')

        if not config_file:
            raise HTTPError(400, 'Missing parameter config_file')

        try:
            self.bed.bind(listen_point, config_file)

            response.status = 200

            return None

        except KeyError as e:
            raise HTTPError(404, 'Listen point %s not found' % e)

        except FileNotFoundError as e:
            raise HTTPError(404, 'File %s not found' % e)

        except ValueError:
            raise HTTPError(500, 'Config mismatch')

        except Exception as e:
            raise HTTPError(500, 'Failed to bind config file to app: %s' % e)

    def create(self, kwargs):
        '''Create an app from the given config string.'''

        config_string = kwargs.get('config_string')

        if not config_string:
            raise HTTPError(400, 'Missing parameter config_string')

        try:
            listen_point = self.bed.create(load(config_string))

            response.status = 201

            return listen_point

        except TypeError:
            raise HTTPError(500, '%s is not a valid config string' % config_string)

        except KeyError as e:
            raise HTTPError(500, 'The %s param is missing in the config' % e)

        except ValueError as e:
            raise HTTPError(409, 'Listen point %s is already taken' % e)

        except Exception as e:
            raise HTTPError(500, 'Failed to create app: %s' % e)

    def remove(self, kwargs):
        '''Remove an app on the given listen point.'''

        listen_point = kwargs.get('listen_point')

        if not listen_point:
            raise HTTPError(400, 'Missing parameter listen_point')

        try:
            self.bed.remove(listen_point)

            response.status = 204

            return None

        except KeyError as e:
            raise HTTPError(404, 'Listen point %s not found' % e)

        except Exception as e:
            raise HTTPError(500, 'Failed to remove app: %s' % e)

    def trigger(self, kwargs):
        '''Trigger action of an app on the given listen point.'''

        listen_point = kwargs.get('listen_point')

        if not listen_point:
            raise HTTPError(400, 'Missing parameter listen_point')

        try:
            params = {key: kwargs[key] for key in kwargs if key not in ('action', 'listen_point')}

            sloth = self.bed.sloths[listen_point]

            sloth.process(params)

            response.status = 202

            return None

        except KeyError as e:
            raise HTTPError(404, 'Listen point %s not found' % e)

        except Exception as e:
            raise HTTPError(500, 'Failed to trigger app actions: %s' % e)

    def info(self, kwargs):
        '''Get information about apps on the given listen points or all apps.'''

        listen_points = kwargs.get('listen_points')

        try:
            if not listen_points:
                app_list = self.bed.sloths.keys()

            elif listen_points == list(listen_points):
                app_list = listen_points

            else:
                app_list = [listen_points]

            info_list = []

            for listen_point in app_list:
                if not listen_point in self.bed.sloths:
                    raise KeyError(listen_point)

                last_build_info = self.history({
                    'listen_point': listen_point,
                    'per_page': 1
                })

                if last_build_info:
                    last_build_status = last_build_info[0]['message']
                    last_build_timestamp = last_build_info[0]['timestamp']

                else:
                    last_build_status = 'Never triggered'
                    last_build_timestamp = 0

                info_list.append({
                    'listen_point': listen_point,
                    'config_file': self.bed.config_files.get(listen_point),
                    'last_build_status': last_build_status,
                    'last_build_timestamp': last_build_timestamp
                })

            info_list.sort(key=lambda record: record['last_build_timestamp'], reverse=True)

            response.status = 200

            return info_list

        except KeyError as e:
            raise HTTPError(404, 'Listen point %s not found' % e)

        except Exception as e:
            raise HTTPError(500, 'Failed to get app info: %s' % e)

    def logs(self, kwargs):
        '''Get paginated app logs from the database.'''

        listen_point = kwargs.get('listen_point')

        if not listen_point:
            raise HTTPError(400, 'Missing parameter listen_point')

        try:
            if not listen_point in self.bed.sloths:
                raise KeyError(listen_point)

            from_page = int(kwargs.get('from_page', 1))
            to_page = int(kwargs.get('to_page', from_page))
            per_page = int(kwargs.get('per_page', 10))
            level = int(kwargs.get('level', 20))

            connection = sqlite3.connect(self.bed.db_path)
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

            response.status = 200

            return logs

        except KeyError as e:
            raise HTTPError(404, 'Listen point %s not found' % e)

        except Exception as e:
            raise HTTPError(500, 'Failed to get app logs: %s' % e)

    def history(self, kwargs):
        '''Get paginated app build history from the database.'''

        listen_point = kwargs.get('listen_point')

        if not listen_point:
            raise HTTPError(400, 'Missing parameter listen_point')

        try:
            from_page = int(kwargs.get('from_page', 1))
            to_page = int(kwargs.get('to_page', from_page))
            per_page = int(kwargs.get('per_page', 10))

            connection = sqlite3.connect(self.bed.db_path)
            cursor = connection.cursor()

            query = 'SELECT * FROM build_history \
                WHERE logger_name=? \
                ORDER BY timestamp DESC \
                LIMIT ? OFFSET ?'

            query_params = (
                listen_point + '.build',
                (to_page - from_page + 1) * per_page,
                (from_page - 1) * per_page
            )

            cursor.execute(query, query_params)

            column_names = [column[0] for column in cursor.description]

            history = [dict(zip(column_names, record)) for record in cursor.fetchall()]

            connection.close()

            response.status = 200

            return history

        except Exception as e:
            raise HTTPError(500, 'Failed to get app build history: %s' % e)

    def version(self, kwargs):
        '''Get the Sloth CI app version.'''

        try:
            version = __version__

            response.status = 200

            return version

        except Exception as e:
            raise HTTPError(500, 'Failed to get Sloth CI server version: %s' % e)

    def restart(self, kwargs):
        '''Ask the Sloth CI server to restart.'''

        try:
            self.bed.bus.restart()

            response.status = 202

            return None

        except Exception as e:
            raise HTTPError(500, 'Failed to restart Sloth CI server: %s' % e)

    def stop(self, kwargs):
        '''Ask the Sloth CI server to stop.'''

        try:
            self.bed.bus.exit()

            response.status = 202

            return None

        except Exception as e:
            raise HTTPError(500, 'Failed to stop Sloth CI server: %s' % e)