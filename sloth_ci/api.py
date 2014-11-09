from cherrypy import expose
from cherrypy import tools
from cherrypy.lib.auth_basic import checkpassword_dict


class API:
    def __init__(self, bed):
        self.bed = bed
        
        auth = self.bed.sconfig['api_auth']

        self.listener = self._make_listener({auth['login']: auth['password']})
    
    def _make_listener(self, auth_dict, realm='sloth-ci'):
        '''Get a basic-auth-protected listener function for the API endpoint.
        
        :param auth_dict: {user: password} dict for authentication
        :param realm: mandatory param for basic auth

        :returns: a CherryPy listener function
        '''
              
        @expose
        @tools.auth_basic(checkpassword=checkpassword_dict(auth_dict), realm=realm)
        def listener(action, params):
            '''Listen to and route API requests.
            
            An API request is an HTTP request with two mandatory parameters: ``action`` and ``params``.

            :param action: string corresponding to one of the available API methods.
            :param params: a single object, a list, or a dict of params for the action.
            '''
            
            if action == 'create_app':
                self.bed.bus.publish('sloth-add', params)

        return listener