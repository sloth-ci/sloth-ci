from subprocess import Popen, TimeoutExpired
from datetime import datetime
from argparse import ArgumentParser
from json import loads
from threading import Thread

import logging

import cherrypy
import requests
import configs


class Sloth:
    """Main Sloth class.

    Each instance represents a separate sloth app,
    with its own config, log, action queue, and queue processor.

    Each app listens for incoming requests on its own URL path.
    """

    def __init__(self, config):
        self.config = config

        self.name = self.config.config_file.split('.')[0]

        file_handler = logging.FileHandler(self.name + '.log', 'a+')
        formatter = logging.Formatter(
            '%(asctime)s | %(name)20s | %(levelname)10s | %(message)s'
        )
        file_handler.setFormatter(formatter)

        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(file_handler)

        self.processing_logger = self.logger.getChild('processing')

        self.queue = []
        self._queue_lock = False

        self.queue_processor = Thread(target=self.process_queue, name=self.name)
        self._processor_lock = False

        self.queue_processor.start()


    def validate_bb_payload(self, payload):
        """Validate Bitbucket payload against repo name and branch.

        :param payload: payload to be validated

        :returns: True of the payload is valid, False otherwise
        """

        if payload == 'test':
            self.processing_logger.info('Payload validated')
            return True

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

        self.processing_logger.info('Executing action: %s', action)

        try:
            process = Popen(action.split(), cwd=self.config['work_dir']).wait()

            self.processing_logger.info('Action executed: %s', action)
            return True

        except TimeoutExpired as e:
            self.processing_logger.critical('Action timed out: %s', e)
            return e

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

    def process_queue(self):
        """Processes execution queue in a separate thread."""

        while not self._processor_lock:
            if self.queue:
                payload, orig = self.queue.pop(0)

                if self.config['actions']:
                    for action in self.config['actions']:
                        self.execute(action)

                if orig and self.config['nodes']:
                    for node in self.config['nodes']:
                        self.broadcast(payload, node)

            elif self._queue_lock:
                return True

            else:
                pass

    def stop(self):
        """Gracefully stops the queue processor.

        New payloads are not added to the queue, existing actions will be finished.
        """
        self._queue_lock = True
        self.logger.info('Stopped.')

    def kill(self):
        """Immediatelly stops the queue processor and clears the queue."""

        self.stop()

        self._processor_lock = True
        self.logger.warning('Killed.')

    @cherrypy.expose
    def listener(self, payload, orig=True):
        """Listens to Bitbucket commit payloads.

        :param payload: Bitbucket commit payload
        """

        if not cherrypy.request.method == 'POST':
            raise cherrypy.HTTPError(405)

        if not self.validate_bb_payload(payload):
            raise cherrypy.HTTPError(400)

        self.logger.info('Payload received')

        if not self._queue_lock:
            self.queue.append((payload, orig))


def run(server_config, sloths):
    """Runs CherryPy loop to listen for payload."""

    cherrypy.config.update({
        'server.socket_host': server_config['host'],
        'server.socket_port': server_config['port']
    })

    for sloth in sloths:
        cherrypy.tree.mount(sloth.listener, sloth.config['listen_to'])
        sloth.logger.info('Mounted')

        cherrypy.engine.autoreload.files.add(sloth.config.config_file)

        cherrypy.engine.subscribe('stop', sloth.stop)

    cherrypy.engine.start()
    cherrypy.engine.block()


def main(server_config_file, default_config_file):
    """Main API function"""

    parser = ArgumentParser()
    parser.add_argument('configs', nargs='+')

    config_files = parser.parse_args().configs
    sloths = [Sloth(configs.load(_, default_config_file)) for _ in config_files]

    server_config = configs.load(server_config_file)

    run(server_config, sloths)

if __name__ == '__main__':
    main('/etc/sloth/server.conf', '/etc/sloth/default.conf')
