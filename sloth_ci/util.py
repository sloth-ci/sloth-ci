from logging import Handler

import sqlite3


class SqliteHandler(Handler):
    '''SQLite handler for the Python logging module.'''

    def __init__(self, db, table):
        super().__init__()

        self.connection = sqlite3.connect(db, check_same_thread=False)
        self.cursor = self.connection.cursor()

        self.table = table

        query = 'CREATE TABLE IF NOT EXISTS %s (timestamp, logger_name, level_name, level_number, message)' % self.table

        self.cursor.execute(query)
        self.connection.commit()

    def emit(self, record):
        query = 'INSERT INTO %s VALUES (?, ?, ?, ?, ?)' % self.table
        query_params = (record.created, record.name, record.levelname, record.levelno, record.msg)

        self.cursor.execute(query, query_params)
        self.connection.commit()

    def close(self):
        self.connection.close()