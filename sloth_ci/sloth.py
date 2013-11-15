from subprocess import Popen
from threading import Thread
from os.path import splitext, basename, abspath, join
from time import sleep

import logging


class Sloth:
    """Main Sloth class.

    Each instance represents a separate sloth app,
    with its own config, log, action queue, and queue processor.

    Each app listens for incoming requests on its own URL path.
    """

    def __init__(self, config):
        self.config = config

        self.name = splitext(basename(self.config.config_full_path))[0]

        file_handler = logging.FileHandler(abspath(join(self.config['log_dir'], self.name + '.log')), 'a+')
        formatter = logging.Formatter(
            '%(asctime)s | %(name)20s | %(levelname)10s | %(message)s'
        )
        file_handler.setFormatter(formatter)

        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(file_handler)

        self.processing_logger = self.logger.getChild('processing')

        self.queue = []
        self._queue_lock = False

        self.queue_processor = Thread(target=self.process_queue, name=self.name)
        self._processor_lock = False

        self.queue_processor.start()

    def is_queue_locked(self):
        return self._queue_lock

    def execute(self, action, data={}):
        """Executes command line command.

        :param action: action to be executed

        :returns: True if successful, Exception otherwise
        """

        self.processing_logger.info('Executing action: %s', action)

        try:
            process = Popen(action.split(), cwd=self.config['work_dir']).wait()

            self.processing_logger.info('Action executed: %s', action)
            return True

        except Exception as e:
            self.processing_logger.critical('Action failed: %s', e)
            return e

    def process_queue(self):
        """Processes execution queue in a separate thread."""

        while not self._processor_lock:
            if self.queue:
                params = self.queue.pop(0)

                if self.config['actions']:
                    for action in self.config['actions']:
                        try:
                            self.execute(action.format_map(params))
                        except KeyError as e:
                            self.processing_logger.critical('Wrong params: %s' % e)
                    else:
                        self.processing_logger.info('Execution queue is empty')

            elif self._queue_lock:
                return True

            else:
                sleep(.25)

    def stop(self):
        """Gracefully stops the queue processor.

        New payloads are not added to the queue, existing actions will be finished.
        """
        self._queue_lock = True
        self.logger.info('Stopped')

    def kill(self):
        """Immediatelly stops the queue processor and clears the queue."""

        self.stop()

        self._processor_lock = True
        self.logger.warning('Killed.')
