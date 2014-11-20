from cherrypy import expose
from cherrypy import tools
from cherrypy import HTTPError, request, response

from cherrypy.lib.auth_basic import checkpassword_dict


class API:
    def __init__(self, bed):
        self.bed = bed
        
        auth = self.bed.config['api_auth']

        self.listener = self._make_listener({auth['login']: auth['password']})
    
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

            if action == 'create':
                if not 'config_string' in kwargs:
                    raise HTTPError(400, 'Missing parameter config_string')
                
                try:
                    listen_point = self.bed.add_sloth(kwargs['config_string'])

                    response.status = 201

                    return listen_point

                except TypeError:
                    raise HTTPError(500, '%s is not a valid config string' % kwargs['config_string'])

                except KeyError as e:
                    raise HTTPError(500, 'The %s param is missing in the config' % e)

                except ValueError as e:
                    raise HTTPError(409, 'Listen point %s is already taken' % e)

                except Exception as e:
                    raise HTTPError(500, 'Failed to create app: %s' % e)

            elif action == 'remove':
                if not 'listen_point' in kwargs:
                    raise HTTPError(400, 'Missing parameter listen_point')
                
                try:
                    self.bed.remove_sloth(kwargs['listen_point'])
                    
                    response.status = 204

                    return None

                except KeyError as e:
                    raise HTTPError(404, 'Listen point %s not found' % e)

                except Exception as e:
                    raise HTTPError(500, 'Failed to remove app: %s' % e)

            elif action == 'trigger':
                if not 'listen_point' in kwargs:
                    raise HTTPError(400, 'Missing parameter listen_point')

                try:
                    params = {_: kwargs[_] for _ in kwargs if _ not in ('action', 'listen_point')}
                    
                    sloth = self.bed.sloths[kwargs['listen_point']]
                    
                    sloth.process(params)

                    response.status = 202

                    return None

                except KeyError as e:
                    raise HTTPError(404, 'Listen point %s not found' % e)

                except Exception as e:
                    raise HTTPError(500, 'Failed to trigger app actions: %s' % e)

            elif action == 'bind':
                if not 'listen_point' in kwargs:
                    raise HTTPError(400, 'Missing parameter listen_point')

                if not 'config_file' in kwargs:
                    raise HTTPError(400, 'Missing parameter config_file')

                try:
                    self.bed.bind_config_file(kwargs['listen_point'], kwargs['config_file'])

                    response.status = 200

                    return None

                except KeyError as e:
                    raise HTTPError(404, 'Listen point %s not found' % e)

                except FileNotFoundError:
                    raise HTTPError(404, 'File %s not found' % e)

                except ValueError:
                    raise HTTPError(500, 'Config mismatch')

                except Exception as e:
                    raise HTTPError(500, 'Failed to bind config file to app: %s' % e)

            elif action == 'info':
                try:
                    if not kwargs.get('listen_point'):
                        app_list = self.bed.sloths.keys()
                
                    else:
                        app_list = [kwargs['listen_point']]
                    
                    info_list = []

                    for listen_point in app_list:
                        if not listen_point in self.bed.sloths:
                            raise KeyError(listen_point)

                        info_list.append({
                            'listen_point': listen_point,
                            'config_file': self.bed.config_files.get(listen_point)
                        })

                    response.status = 200

                    return info_list

                except KeyError as e:
                    raise HTTPError(404, 'Listen point %s not found' % e)

                except Exception as e:
                    raise HTTPError(500, 'Failed to get app info: %s' % e)

            elif action == 'restart':
                try:
                    self.bed.bus.restart()

                    response.status = 202

                    return None
                
                except Exception as e:
                    raise HTTPError(500, 'Failed to restart Sloth CI server: %s' % e)

            elif action == 'stop':
                try:
                    self.bed.bus.exit()

                    response.status = 202

                    return None

                except Exception as e:
                    raise HTTPError(500, 'Failed to stop Sloth CI server: %s' % e)

            else:
                raise HTTPError(404, 'Action not found')
                

        return listener