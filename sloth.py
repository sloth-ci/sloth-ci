from subprocess import call
from datetime import datetime
from argparse import ArgumentParser
from json import loads
from hashlib import md5
import sqlite3
import os.path
import logging

import cherrypy
import requests
import configs


class Sloth:
    def __init__(self, config):
        self.config = config

        file_handler = logging.FileHandler(self.config['prefs']['log_file'], 'a+')
        formatter = logging.Formatter(
            '%(asctime)s | %(name)20s | %(levelname)10s | %(message)s'
        )
        file_handler.setFormatter(formatter)

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(file_handler)

        self.processing_logger = self.logger.getChild('processing')

    def validate_bb_payload(self, payload):
        """Validate Bitbucket payload against repo name and branch.

        :param payload: payload to be validated

        :returns: True of the payload is valid, False otherwise
        """

        try:
            parsed_payload = loads(payload)

            repo = parsed_payload['repository']['owner'] + '/' + parsed_payload['repository']['slug']
            branch = parsed_payload['commits'][-1]['branch']

            if repo == self.config['repo'] and branch == self.config['branch']:
                self.processing_logger.info('Payload validated')
                return True
            elif repo != self.config['repo']:
                self.processing_logger.info('Payload validation failed: repo mismatch.')
                return False
            elif branch != self.config['branch']:
                self.processing_logger.info('Payload validation failed: branch mismatch.')
                return False
        except:
            self.processing_logger.info('Payload validation failed.')
            return False

    def execute(self, action):
        """Executes command line command.

        :param action: action to be executed

        :returns: True if successful, Exception otherwise
        """

        try:
            call(action.split())

            self.processing_logger.info('Action executed: %s', action)

            return True
        except Exception as e:
            self.processing_logger.critical('Action failed: %s', e)

            return e

    def broadcast(self, payload, node):
        """Transmit payload to a node.

        :param payload: payload to be transmitted
        :param node: complete node URL (with protocol and port, **with** the path to the sloth listener)

        :returns: response code
        """

        try:
            r = requests.post('%s' % node, data={'payload': payload, 'orig': False})

            if r.status_code == 200:
                self.processing_logger.info('Payload broadcasted to %s', node)
            else:
                self.processing_logger.warning('Broadcasting to %s failed: %s', node, r.status)

            return True
        except Exception as e:
            self.processing_logger.warning('Broadcasting to %s failed: %s', node, e)
            return e

    @cherrypy.expose
    def listener(self, payload, orig=True):
        """Listens to Bitbucket commit payloads.

        :param payload: Bitbucket commit payload
        """

        if not cherrypy.request.method == 'POST':
            raise cherrypy.HTTPError(405)

        self.logger.info('Payload received')

        if not self.validate_bb_payload(payload):
            raise cherrypy.HTTPError(400)

        if self.config['actions']:
            for action in self.config['actions']:
                self.execute(action)

        if orig and self.config['nodes']:
            for node in self.config['nodes']:
                self.broadcast(payload, node)

def run(sloths):
    """Runs CherryPy loop to listen for payload."""

    cherrypy.config.update({
        'server.socket_host': sloths[0].config['server']['host'],
        'server.socket_port': sloths[0].config['server']['port']
    })

    for sloth in sloths:
        cherrypy.tree.mount(sloth.listener, sloth.config['server']['path'])
        cherrypy.engine.autoreload.files.add(sloth.config.config_file)

    cherrypy.engine.start()
    cherrypy.engine.block()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-c', '--config', nargs='+')

    config_files = parser.parse_args().config or ['sloth.conf']

    sloths = [Sloth(configs.load(config_file, 'sloth.conf')) for config_file in config_files]

    run(sloths)
