from subprocess import call
from datetime import datetime
from argparse import ArgumentParser

import cherrypy
import requests
import configs


def log(func):
    """Logger decorator"""

    def logged(*args, **kwargs):
        with open('sloth.log', 'a') as log:
            log.writelines(
                '%s -- %s(%s, %s): %s\n' % (
                    datetime.now().ctime(),
                    func.__name__,
                    args,
                    kwargs,
                    func(*args, **kwargs)
                )
            )

    return logged


@log
def execute(action):
    """Executes command line command.

    :param action: action to be executed

    :returns: 'OK' if successful, Exception otherwise
    """

    action = action.format(
        work_dir = config['work_dir'],
        branch = config['branch']
    )

    try:
        call(action.split())
        return 'OK'
    except Exception as e:
        return e


@log
def transmit(payload, node):
    """Transmit payload to a node.

    :param payload: payload to be transmitted
    :param node: complete node URL (with protocol and port, **without** the ``/sloth`` suffix)

    :returns: response code
    """

    return requests.post('%s/sloth' % node, data={'payload': payload, orig: False})


def validate_bb_payload(payload):
    pass

@cherrypy.expose
def listen(payload, orig=True):
    """Listens to Bitbucket commit payloads.

    :param payload: BitBucket commit payload
    """

    #only POST requests are considered valid
    if not cherrypy.request.method == 'POST':
            raise cherrypy.HTTPError(405)

    print(payload)

    if config['actions']:
        for action in config['actions']:
            execute(action)

    if orig and config['nodes']:
        for node in config['nodes']:
            transmit(payload, node)


if __name__ == '__main__':
    """Runs main loop"""

    parser = ArgumentParser()
    parser.add_argument('-c', '--config')

    config_file = parser.parse_args().config or 'sloth.conf'

    config = configs.load(config_file)

    cherrypy.config.update({
        'server.socket_host': config['host'],
        'server.socket_port': config['port'],
    })

    cherrypy.quickstart(listen, '/sloth')
