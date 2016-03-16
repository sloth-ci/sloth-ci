def extend_bed(cls, extension):
    '''Add routes and handlers for the API methods.

    :param cls: base :class:`Bed <sloth_ci.bed.Bed>` class to be extended
    :param extension: ``{'api': {'module': 'api'}}``

    :returns: extended :class:`Bed <sloth_ci.bed.Bed>` class
    '''

    import cherrypy
    from cherrypy.lib.auth_basic import checkpassword_dict

    from yaml import load

    import sqlite3

    from ... import __version__


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

            for alias in ('auth', 'api_auth'):
                auth = self.config.get(alias)
                if auth:
                    try:
                        auth_dict = {entry['login']:entry['password'] for entry in auth}

                    except TypeError:
                        auth_dict = {auth['login']: auth['password']}

                    finally:
                        break
            else:
                cherrypy.log.error('Warning: Unprotected API access')
                auth_dict = {}

            api_listener = self._api_listener

            if auth_dict:
                api_listener._cp_config.update({
                    'tools.auth_basic.on': True,
                    'tools.auth_basic.realm': 'sloth-ci',
                    'tools.auth_basic.checkpassword': checkpassword_dict(auth_dict),
                })

            self._dispatcher.connect('api', '/', api_listener)

        @cherrypy.expose
        @cherrypy.tools.json_out()
        def _api_listener(self, action, **kwargs):
            '''Listen to and route API requests.

            An API request is a GET or POST HTTP request with one mandatory param ``action`` and
            additional params for the given action.

            Params can be provided in the URL or as form data.

            :param action: string corresponding to one of the available API methods.
            :param kwargs: params for the given action.
            '''

            cherrypy.request.error_page = {'default': lambda status, message, traceback, version: message}

            try:
                return self.actions[action](kwargs)

            except KeyError as e:
                raise cherrypy.HTTPError(404, 'Action %s not found' % e)

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
                if listen_point not in self.sloths:
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
                params = {key: kwargs[key] for key in kwargs if key not in ('listen_point', 'wait')}

                sloth = self.sloths[listen_point]

                sloth.process(params)

                if not kwargs.get('wait'):
                    cherrypy.response.status = 202
                    return None

                else:
                    sloth.queue_processor.join()
                    info = self.info({'listen_point': listen_point})
                    build_successful = info['last_build_status_level'] == 'INFO'

                    success_url, fail_url = kwargs.get('success_url'), kwargs.get('fail_url')

                    if build_successful and success_url:
                        raise cherrypy.HTTPRedirect(success_url)

                    elif not build_successful and fail_url:
                        raise cherrypy.HTTPRedirect(fail_url)

                    else:
                        return self.info({'listen_point': listen_point})['last_build_status_message']

            except KeyError as e:
                raise cherrypy.HTTPError(404, 'Listen point %s not found' % e)

            except cherrypy.HTTPRedirect as e:
                raise e

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