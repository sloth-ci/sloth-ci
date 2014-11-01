from cherrypy import expose
from cherrypy import tools
from cherrypy.lib.auth_basic import checkpassword_dict


class API:
    def __init__(self, sconfig):
        auth = sconfig['api_auth']

        self.listener = self._make_listener({auth['login']: auth['password']})
    
    def _make_listener(self, auth_dict, realm='sloth-ci'):
        '''Get a basic-auth-protected listener function for the API endpoint.
        
        :param auth_dict: {user: password} dict for authentication
        :param realm: mandatory param for basic auth

        :returns: a CherryPy listener function
        '''
              
        @expose
        @tools.auth_basic(checkpassword=checkpassword_dict(auth_dict), realm=realm)
        def listener(**kwargs):
            print(kwargs)
            self.process_request(kwargs)

        return listener

    def process_request(self, request):
        action = request['action']
        params = request.get('params')

        print(action, params)