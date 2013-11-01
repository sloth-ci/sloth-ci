"""
************
sloth_ci.api
************

This module implements the sloth API.
"""


from importlib import import_module

from argparse import ArgumentParser

import cherrypy
from configs import load

from .sloth import Sloth


def make_listener(sloth):

    @cherrypy.expose
    def listener(payload, orig=True):
        """Listens to payloads.

        :param payload: payload
        """

        if not cherrypy.request.method == 'POST':
            raise cherrypy.HTTPError(405)
        sloth.logger.info('Payload received from %s - %s' % (cherrypy.request.headers['Remote-Addr'], cherrypy.request.headers['User-Agent']))

        try:
            validator = import_module(
                '.validators.%s' % sloth.config['provider'],
                package=__package__
            )

        except ImportError as e:
            sloth.logger.critical('No matching validator found: %s' % e)
            raise cherrypy.HTTPError(500)

        payload_valid, validation_message = validator.validate(payload, sloth.config['provider_data'])

        sloth.logger.info(validation_message)

        if not payload_valid:
            raise cherrypy.HTTPError(400)


        if not sloth.is_queue_locked():
            sloth.queue.append((payload, orig))

    return listener


def run(host, port, log_dir, sloths):
    """Runs CherryPy loop to listen for payload."""


    from os.path import abspath, join

    from cherrypy.process.plugins import Daemonizer
    d = Daemonizer(cherrypy.engine).subscribe()

    cherrypy.config.update(
        {
            'environment': 'production',
            'server.socket_host': host,
            'server.socket_port': port,
            'log.access_file': abspath(join(log_dir, 'access.log')),
            'log.error_file': abspath(join(log_dir, 'error.log'))
        }
    )

    for sloth in sloths:
        cherrypy.tree.mount(make_listener(sloth), sloth.config['listen_to'])

        sloth.logger.info('Mounted at %s' % sloth.config['listen_to'])

        cherrypy.engine.autoreload.files.add(sloth.config.config_full_path)

        cherrypy.engine.subscribe('stop', sloth.stop)

    cherrypy.engine.start()
    cherrypy.engine.block()


def main():
    """Main API function"""

    parser = ArgumentParser()
    parser.add_argument('--host', required=True)
    parser.add_argument('--port', type=int, required=True)
    parser.add_argument('--log_dir', required=True)
    parser.add_argument('config', nargs='+')

    host, port, log_dir = parser.parse_args().host, parser.parse_args().port, parser.parse_args().log_dir

    config_files = parser.parse_args().config

    sloths = [Sloth(load(config_file, defaults={'log_dir': log_dir})) for config_file in config_files]

    run(host, port, log_dir, sloths)
