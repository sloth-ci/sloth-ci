def extend_sloth(cls, extension):
    '''Add SQLite logging for build events.

    :param cls: base :mod:`Sloth <sloth_ci.sloth.Sloth>` class to extend
    :param extension: ``{'build_history': {'module': 'db.builds', 'db': self.db_path, 'table': 'build_history'}}``

    :returns: extended :mod:`Sloth <sloth_ci.sloth.Sloth>` class
    '''

    from .util import SqliteHandler


    class Sloth(cls):
        def __init__(self, config):
            super().__init__(config)

            db_build_log_config = extension['config']

            db_build_log_handler = SqliteHandler(db_build_log_config['db'], db_build_log_config['table'])

            self.build_logger.addHandler(db_build_log_handler)

            self.log_handlers[extension['name']] = db_build_log_handler

        def stop(self):
            super().stop()
            self.build_logger.removeHandler(self.log_handlers.pop(extension['name']))


    return Sloth
