from subprocess import call
from datetime import datetime
from argparse import ArgumentParser
from json import loads
from functools import wraps

import cherrypy
import requests
import configs


def log(func):
    """Logger decorator"""

    @wraps(func)
    def logged(*args, **kwargs):
        result = func(*args, **kwargs)

        try:
            with open('sloth.log', 'r') as log:
                pass
        except:
            with open('sloth.log', 'w') as log:
                pass

        with open('sloth.log', 'a') as log:
            log.writelines(
                '%s -- %s(%s, %s): %s\n' % (
                    datetime.now().ctime(),
                    func.__name__,
                    args,
                    kwargs,
                    result
                )
            )

        return result

    return logged


class Sloth:
    def __init__(self, config):
        self.config = config

    @log
    def validate_bb_payload(self, payload):
        """Validate Bitbucket payload against repo name and branch.

        :param payload: payload to be validated

        :returns: True of the payload is valid, False otherwise
        """

        try:
            payload = loads(payload)

            repo = payload['repository']['owner'] + '/' + payload['repository']['slug']
            branch = payload['commits'][0]['branch']

            return repo == self.config['repo'] and branch == self.config['branch']
        except:
            return False

    @log
    def execute(self, action):
        """Executes command line command.

        :param action: action to be executed

        :returns: 'OK' if successful, Exception otherwise
        """

        action = action.format(
            work_dir = self.config['work_dir'],
            branch = self.config['branch']
        )

        try:
            call(action.split())
            return 'OK'
        except Exception as e:
            return e


    @log
    def transmit(self, payload, node):
        """Transmit payload to a node.

        :param payload: payload to be transmitted
        :param node: complete node URL (with protocol and port, **without** the ``/sloth`` suffix)

        :returns: response code
        """

        return requests.post('%s/sloth' % node, data={'payload': payload, 'orig': False})

    def get_listener(self):
        """Create listener for the CherryPy main loop."""

        @cherrypy.expose
        def listener(payload, orig=True):
            """Listens to Bitbucket commit payloads.

            :param payload: BitBucket commit payload
            """

            #only POST requests are considered valid
            if not cherrypy.request.method == 'POST':
                raise cherrypy.HTTPError(405)

            if cherrypy.request.headers['User-Agent'] != 'Bitbucket.org' or not self.validate_bb_payload(payload):
                raise cherrypy.HTTPError(400)

            if self.config['actions']:
                for action in self.config['actions']:
                    self.execute(action)

            if orig and self.config['nodes']:
                for node in self.config['nodes']:
                    self.transmit(payload, node)

        return listener

    def listen(self, path='/sloth'):
        """Runs CherryPy loop to listen for payload."""

        cherrypy.config.update({
            'server.socket_host': self.config['host'],
            'server.socket_port': self.config['port'],
        })

        cherrypy.quickstart(self.get_listener(), path)


if __name__ == '__main__':
    """Runs main loop"""

    parser = ArgumentParser()
    parser.add_argument('-c', '--config')

    config_file = parser.parse_args().config or 'sloth.conf'

    config = configs.load(config_file)

    sloth = Sloth(config)

    sloth.listen()
