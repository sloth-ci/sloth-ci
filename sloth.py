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

from mako.template import Template
from mako.lookup import TemplateLookup


class Sloth:
    def __init__(self, config):
        self.config = config
        self.lookup = TemplateLookup(directories=self.config['server']['webface_dir'])

        file_handler = logging.FileHandler(self.config['log'], 'a+')
        formatter = logging.Formatter(
            '%(asctime)s | %(name)20s | %(levelname)10s | %(message)s'
        )
        file_handler.setFormatter(formatter)

        self.logger = logging.getLogger('__name__')
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

        :returns: 'OK' if successful, Exception otherwise
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

    def user_validate_credentials(self, login, password):
        """Validates webface login credentials.

        :param login: Login
        :param password: Password

        :returns: True if the credentials are valid, False otherwise
        """

        if not login or not password:
            return False

        with sqlite3.connect(self.config['db']) as db_connection:
            db_cursor = db_connection.cursor()

            db_cursor.execute('CREATE TABLE IF NOT EXISTS Users(Id INTEGER PRIMARY KEY, Login TEXT, Hash TEXT, Status CHAR)')

            try:
                hash, status = db_cursor.execute('SELECT Hash, Status from Users WHERE Login = ?', (login,)).fetchone()
            except:
                return False

        if status == 'A' and md5(password.encode()).hexdigest() == hash:
            return True

        return False

    def user_register(self, r_login, r_password):
        """Registers new webface user.

        :param r_login: Login
        :param r_password: Password
        """

        with sqlite3.connect(self.config['db']) as db_connection:
            db_cursor = db_connection.cursor()

            r_hash = md5(r_password.encode()).hexdigest()

            r_status = db_cursor.execute('SELECT * FROM Users').fetchone() and 'P' or 'A'

            db_cursor.execute('INSERT INTO Users(Login, Hash, Status) VALUES (?, ?, ?)', (r_login, r_hash, r_status))

            db_connection.commit()

    def user_update(self, user_statuses):
        """Updates user statuses.

        :param user_statuses: Dictionary of user ID and status to set
        """

        with sqlite3.connect(self.config['db']) as db_connection:
            db_cursor = db_connection.cursor()

            for uid, status in user_statuses.items():
                db_cursor.execute('UPDATE Users SET Status = ? WHERE Id = ?', (status, uid))

            db_connection.commit()

    def get_log_lines(self):
        """Read lines from the log file in reverse and format them to a dictionaries.

        :yields: {'timestamp': timestamp, 'name': logger name, 'level': message level, 'message': message text}
        """

        for line in reversed(open(self.config['log']).readlines()):
            yield dict(
                zip(
                    [
                        'timestamp',
                        'name',
                        'level',
                        'message'
                    ],
                    list(map(lambda __: __.strip(), line.split('|')))
                )
            )

    def get_users(self):
        """Gets users and formats them to dictionaries

        :yields: {'id': uid, 'login': login, 'status', status ('A' or 'P')}
        """

        with sqlite3.connect(self.config['db']) as db_connection:
            db_cursor = db_connection.cursor()

            db_cursor.execute('CREATE TABLE IF NOT EXISTS Users(Id INTEGER PRIMARY KEY, Login TEXT, Hash TEXT, Status CHAR)')

            for uid, login, status in db_cursor.execute('SELECT Id, Login, Status from Users'):
                yield {'id': uid, 'login': login, 'status': status}

    @cherrypy.expose
    def webface(self, login=None, password=None, r_login=None, r_password=None, r_password2=None, **user_statuses):
        """Renders webface.

        Handles signins and signups, user status updating.

        """

        if cherrypy.request.method == 'GET':
            tmpl = self.lookup.get_template('login.html')

            return tmpl.render()

        elif cherrypy.request.method == 'POST':
            if self.user_validate_credentials(login, password) or self.user_validate_credentials(r_login, r_password):
                tmpl = self.lookup.get_template('index.html')

                lines = self.get_log_lines()

                users = self.get_users()

                return tmpl.render(login=login, lines=lines, users=users)

            elif r_login and r_password == r_password2:
                self.user_register(r_login, r_password)

            elif user_statuses:
                self.user_update(user_statuses)

            raise cherrypy.HTTPRedirect(self.config['server']['path'] + '/webface/')
        else:
            raise cherrypy.HTTPError(405)

    def run(self):
        """Runs CherryPy loop to listen for payload."""

        cherrypy.config.update({
            'server.socket_host': self.config['server']['host'],
            'server.socket_port': self.config['server']['port']
        })

        cherrypy.tree.mount(self.listener, self.config['server']['path'])

        cherrypy.tree.mount(
            self.webface,
            self.config['server']['path'] + '/webface',
            {
                '/': {
                    'tools.staticdir.root': os.path.abspath(self.config['server']['webface_dir']),
                    'tools.staticdir.on': True,
                    'tools.staticdir.dir': ''
                }
            }
        )

        cherrypy.engine.autoreload.files.add(self.config.config_file)

        cherrypy.engine.start()
        cherrypy.engine.block()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-c', '--config')

    config_file = parser.parse_args().config

    config = configs.load(config_file, 'sloth.conf')

    Sloth(config).run()
