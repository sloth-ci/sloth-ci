"""
***********
sloth.api
***********

This module implements the sloth API.
"""

from argparse import ArgumentParser

import cherrypy
from configs import load

from .sloth import Sloth
from .validators import validate

def make_listener(sloth):

    @cherrypy.expose
    def listener(payload, orig=True):
        """Listens to Bitbucket commit payloads.

        :param payload: Bitbucket commit payload
        """

        if not cherrypy.request.method == 'POST':
            raise cherrypy.HTTPError(405)
        sloth.logger.info('Payload received from %s - %s' % (cherrypy.request.headers['Remote-Addr'], cherrypy.request.headers['User-Agent']))

        payload_valid, validation_message = validate[sloth.config['provider']](payload, sloth.config['provider_data'])

        if not payload_valid:
            raise cherrypy.HTTPError(400)

        sloth.logger.info(validation_message)

        if not sloth.queue_lock:
            sloth.queue.append((payload, orig))

    return listener


def run(server_config, sloths):
    """Runs CherryPy loop to listen for payload."""

    cherrypy.config.update({
        'server.socket_host': server_config['host'],
        'server.socket_port': server_config['port']
        })

    for sloth in sloths:
        cherrypy.tree.mount(make_listener(sloth), sloth.config['listen_to'])
        sloth.logger.info('Mounted')

        cherrypy.engine.autoreload.files.add(sloth.config.config_file)

        cherrypy.engine.subscribe('stop', sloth.stop)

        cherrypy.engine.start()
        cherrypy.engine.block()


def main(default_server_config_file, default_config_file):
    """Main sloth API function"""

    parser = ArgumentParser()
    parser.add_argument('configs', nargs='+')
    parser.add_argument('-s', '--server_config', required=False)

    config_files = parser.parse_args().configs
    sloths = [Sloth(load(_, default_config_file)) for _ in config_files]

    server_config_file = parser.parse_args().server_config or default_server_config_file
    server_config = load(server_config_file)

    run(server_config, sloths)
