def extend(cls, extension):
    from os.path import abspath, join, exists
    from os import makedirs

    import logging

    from ..util import SqliteHandler


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