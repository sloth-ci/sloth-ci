from subprocess import call
from datetime import datetime
from argparse import ArgumentParser
from json import loads
from functools import wraps
from hashlib import md5
import sqlite3
import os.path

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
            branch = payload['commits'][-1]['branch']

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
    def broadcast(self, payload, node):
        """Transmit payload to a node.

        :param payload: payload to be transmitted
        :param node: complete node URL (with protocol and port, **without** the ``/sloth`` suffix)

        :returns: response code
        """

        return requests.post('%s/sloth' % node, data={'payload': payload, 'orig': False})

    @cherrypy.expose
    def listener(self, payload, orig=True):
        """Listens to Bitbucket commit payloads.

        :param payload: Bitbucket commit payload
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
                self.broadcast(payload, node)

    def validate_credentials(self, login, password):
        """Validate webface login credentials.

        :param login: login
        :param password: password

        :returns: True if the credentials are valid, False otherwise
        """

        if not login or not password:
            return False

        db_connection = sqlite3.connect(self.config['db'])
        db_cursor = db_connection.cursor()

        db_cursor.execute('CREATE TABLE IF NOT EXISTS Users(Id INTEGER PRIMARY KEY, Login TEXT, Hash TEXT)')

        hash = db_cursor.execute('SELECT Hash from Users WHERE Login=?', (login,)).fetchone()

        if not hash:
            return False

        if md5(password.encode()).hexdigest() != hash[0]:
            return False

        return True

    @cherrypy.expose
    def webface(self, login=None, password=None):
        if cherrypy.request.method == 'GET':
            return open('webface/login.html', 'r')
        elif cherrypy.request.method == 'POST':
            if self.validate_credentials(login, password):
                return open('sloth.log', 'r')
            else:
                raise cherrypy.HTTPRedirect(self.config['server']['path'] + '/webface')
        else:
            raise cherrypy.HTTPError(405)

    def run(self):
        """Runs CherryPy loop to listen for payload."""

        cherrypy.config.update({
            'server.socket_host': self.config['server']['host'],
            'server.socket_port': self.config['server']['port'],
        })

        cherrypy.tree.mount(self.listener, self.config['server']['path'])
        cherrypy.tree.mount(
            self.webface,
            self.config['server']['path'] + '/webface',
            {
                '/': {
                    'tools.staticdir.root': '/home/moigagoo/projects/sloth/webface',
                    'tools.staticdir.on': True,
                    'tools.staticdir.dir': ''
                }
            }
        )

        cherrypy.engine.start()
        cherrypy.engine.block()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-c', '--config')

    config_file = parser.parse_args().config

    config = configs.load(config_file, 'sloth.conf')

    Sloth(config).run()
