from cherrypy import expose
from cherrypy import tools
from cherrypy import HTTPError, request

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
        def listener(action, **kwargs):
            '''Listen to and route API requests.
            
            An API request is an HTTP request with two mandatory parameters: ``action`` and ``params``.

            :param action: string corresponding to one of the available API methods.
            :param params: a single object, a list, or a dict of params for the action.
            '''

            request.error_page = {'default': self._handle_error}

            if action == 'create-app':
                if not 'config_source' in kwargs:
                    raise HTTPError(400, 'Missing parameter config_source')
                
                try:
                    return self.bed.add_sloth(kwargs['config_source'])

                except KeyError as e:
                    raise HTTPError(500, 'The %s param is missing in the config' % e)

                except ValueError as e:
                    raise HTTPError(409, 'Listen point %s is already taken' % e)

                except Exception as e:
                    raise HTTPError(500, 'Could not create app: %s' % e)

            elif action == 'remove-app':
                if not 'listen_point' in kwargs:
                    raise HTTPError(400, 'Missing parameter listen_point')
                
                try:
                    return self.bed.remove_sloth(kwargs['listen_point'])

                except KeyError as e:
                    raise HTTPError(404, 'Listen point %s not found' % e)

            elif action == 'restart':
                self.bed.bus.restart()
                return('Restarting Sloth CI')

            elif action == 'stop':
                self.bed.bus.exit()
                return('Stopping Sloth CI')

            else:
                raise HTTPError(404, 'Invalid action')
                

        return listener