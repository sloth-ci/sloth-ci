from subprocess import Popen, PIPE, TimeoutExpired
from threading import Thread
from os.path import splitext, basename, abspath, join
from time import sleep
from collections import deque
from importlib import import_module
import logging


class Sloth:
    '''Base Sloth class.

    Each instance represents a separate Sloth app,
    with its own config, log, action queue, and queue processor.

    Each app listens for incoming requests on its own URL path.
    '''

    extensions = []

    def __init__(self, config):
        self.config = config

        self.name = splitext(basename(self.config.config_full_path))[0]

        self.queue = deque()
        self._queue_lock = False

        self.queue_processor = Thread(target=self.process_queue, name=self.name)
        self._processor_lock = False

        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.INFO)
        self.processing_logger = self.logger.getChild('processing')

    @classmethod
    def extend(cls, extensions):
        '''Sequentially chain-inherit Sloth classes from extensions.
    
        The first extension's Sloth class inherits from the base Sloth class and becomes the base class, then the second one inherits from it, and so on.

        :params extensions: list of extensions to load.
    
        :returns: ExtendedSloth is a Sloth class inherited from all extensions' Sloth classes; errors—list of errors raised during the extensions loading.
        '''
    
        ExtendedSloth = cls
        errors = []

        if extensions:
            for extension in extensions:
                try:
                    ext = import_module('.ext.%s' % extension, package=__package__)
            
                    ExtendedSloth = ext.extend(ExtendedSloth)

                    cls.extensions.append(extension)

                except Exception as e:
                    errors.append('Could not load extension %s: %s' % (extension, e))

        return ExtendedSloth, errors

    def start(self):
        '''Starts the queue processor.'''

        self.queue_processor.start()

    def is_queue_locked(self):
        '''Tells if the processing queue is locked.'''

        return self._queue_lock

    def execute(self, action):
        '''Executes command line command.

        :param action: action to be executed

        :returns: True if successful, Exception otherwise
        '''

        self.processing_logger.info('Executing action: %s', action)

        try:
            process = Popen(
                action.split(),
                cwd=self.config.get('work_dir') or '.',
                stdout=PIPE,
                stderr=PIPE)

            stdout, stderr = process.communicate(timeout=self.config.get('exec_timeout'))
            
            self.processing_logger.debug(bytes.decode(stdout))
            self.processing_logger.debug(bytes.decode(stderr))

            self.processing_logger.info('Action executed: %s', action)
            
            return True

        except TimeoutExpired:
            process.kill()

            stdout, stderr = process.communicate()
            
            self.processing_logger.debug(bytes.decode(stdout))
            self.processing_logger.debug(bytes.decode(stderr))

            raise

        except Exception:
            raise

    def process_queue(self):
        '''Processes execution queue in a separate thread.'''

        while not self._processor_lock:
            if self.queue:
                params = self.queue.popleft()

                if self.config['actions']:
                    for action in self.config['actions']:
                        try:
                            self.execute(action.format_map(params))

                        except KeyError as e:
                            self.processing_logger.critical('Unknown param in action: %s', e)

                            if self.config.get('stop_on_first_fail'):
                                break

                        except Exception as e:
                            self.processing_logger.critical('Action failed: %s', e)

                            if self.config.get('stop_on_first_fail'):
                                break
                    else:
                        self.processing_logger.info('Execution queue is empty')

            elif self._queue_lock:
                return True

            else:
                sleep(.25)

    def stop(self):
        '''Gracefully stops the queue processor.

        New payloads are not added to the queue, existing actions will be finished.
        '''

        self._queue_lock = True
        self.logger.info('Stopped')

    def kill(self):
        '''Immediatelly stops the queue processor and clears the queue.'''

        self.stop()

        self._processor_lock = True
        self.logger.warning('Killed.')
