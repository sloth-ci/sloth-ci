def extend_sloth(cls, extension):
    '''Add SQLite logging for all app events.

    :param cls: base :mod:`Sloth <sloth_ci.sloth.Sloth>` class to extend
    :param extension: ``{'app_logs': {'module': 'db.logs', 'db': self.db_path, 'table': 'app_logs'}``

    :returns: extended :mod:`Sloth <sloth_ci.sloth.Sloth>` class
    '''

    import logging

    from .util import SqliteHandler


    class Sloth(cls):
        def __init__(self, config):
            super().__init__(config)

            db_app_log_config = extension['config']

            db_app_log_handler = SqliteHandler(db_app_log_config['db'], db_app_log_config['table'])

            db_app_log_handler.setLevel(logging.DEBUG)

            self.logger.addHandler(db_app_log_handler)

            self.log_handlers[extension['name']] = db_app_log_handler

        def stop(self):
            super().stop()
            self.logger.removeHandler(self.log_handlers.pop(extension['name']))


    return Sloth
