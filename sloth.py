from subprocess import call
from datetime import datetime

import cherrypy
import requests
import configs

import  sloth_conf

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
        work_dir = sloth_conf.work_dir,
        branch = sloth_conf.branch
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

    return requests.post('%s/sloth' % node, data={'payload': payload})


@cherrypy.expose
def listen(payload):
    """Listens to Bitbucket commit payloads.

    :param payload: BitBucket commit payload
    """

    #only POST requests are considered valid
    if not cherrypy.request.method == 'POST':
            raise cherrypy.HTTPError(405)

    for action in sloth_conf.actions:
        execute(action)

    for node in sloth_conf.nodes:
        transmit(payload, node)


if __name__ == '__main__':
    """Runs main loop"""

    cherrypy.config.update({
        'server.socket_host': sloth_conf.host,
        'server.socket_port': sloth_conf.port,
    })

    cherrypy.quickstart(listen, '/sloth')
