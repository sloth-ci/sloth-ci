from yaml import load
from requests import post, exceptions


class API:
    def __init__(self, config):
        self.url = 'http://%s:%d' % (config['host'], config['port'])
        self.auth = (config['api_auth']['login'], config['api_auth']['password'])

    def _send_api_request(self, data={}):
        '''Send a POST request to the Sloth CI API with the given data.'''

        try:
            response = post(self.url, auth=self.auth, data=data)

            if response.ok:
                if response.content:
                    content = response.json()

                else:
                    content = None

            else:
                content = response.text.strip()

            return response.status_code, content
        
        except exceptions.ConnectionError:
            raise ConnectionError('Failed to connect to Sloth CI on %s' % self.url)

    def bind(self, listen_point, config_file):
        '''Bind a Sloth app with a config file.
 
        :param listen_point: app's listen point
        :param config_file: absolute path to the config file
        '''
        
        data = {
            'action': 'bind',
            'listen_point': listen_point,
            'config_file': config_file
        }
        
        status, content = self._send_api_request(data)

        if status == 200:
            return True

        elif status == 404:
            raise KeyError(content)

        else:
            raise RuntimeError(content)

    def create(self, config_file):
        '''Create an app from the config file.
        
        :param config_file: path to the app config file
        '''

        data = {
            'action': 'create',
            'config_string': ''.join(open(config_file).readlines()),
        }

        status, content = self._send_api_request(data)

        if status == 201:
            return content

        elif status == 409:
            raise ValueError(content)
            
        else:
            raise RuntimeError(content)

    def remove(self, listen_point):
        '''Remove an app on a certain listen point.
        
        :param listen_point: the app's listen point
        '''

        data = {
            'action': 'remove',
            'listen_point': listen_point
        }

        status, content = self._send_api_request(data)
        
        if status == 204:
            return True

        elif status == 404:
            raise KeyError(content)

        else:
            raise RuntimeError(content)

    def trigger(self, listen_point, params={}):
        '''Trigger actions of a particular app to execute with the given params.

        :param listen_point: app's listen point
        :param params: dict of params
        '''

        data = {
            'action': 'trigger',
            'listen_point': listen_point,
        }

        data.update(params)
        
        status, content = self._send_api_request(data)

        if status == 202:
            return True

        elif status == 404:
            raise KeyError(content)

        else:
            raise RuntimeError(content)

    def info(self, listen_points=[]):
        '''Get info for a particular app or all apps.
 
        :param listen_points: list of app listen points to show info for; if empty, all apps will be shown
        
        :returns: list of dicts with keys listen_point and config_file
        '''

        data = {
            'action': 'info',
            'listen_points': listen_points
        }

        status, content = self._send_api_request(data)

        if status == 200:
            return content

        elif status == 404:
            raise KeyError(content)

        else:
            raise RuntimeError(content)

    def restart(self):
        '''Ask a a Sloth CI server to restart.'''

        status, content = self._send_api_request({'action': 'restart'})
        
        if status == 202:
            return True

        else:
            raise RuntimeError(content)

    def stop(self):
        '''Ask a a Sloth CI server to stop.'''

        status, content = self._send_api_request({'action': 'stop'})
        
        if status == 202:
            return True

        else:
            raise RuntimeError(content)