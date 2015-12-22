'''Describe your extension.


Installation
------------

.. code-block:: bash

    $ pip install sloth-ci.ext.spam


Usage
-----

.. code-block:: yaml
    :caption: spam.yml

    extensions:
        spam:
            # Use the module sloth_ci.ext.spam.
            module: spam
            param1: value1
            param2: value2
            ...
'''

__title__ = 'sloth-ci.ext.spam'
__description__ = 'Describe your extension'
__version__ = '0.0.1'
__author__ = 'Your Name'
__author_email__ = 'your@email.com'
__license__ = 'MIT'


def extend_bed(cls, extension):
    '''Modify ``sloth_ci.bed.Bed`` to add API endpoints and custom URI handlers.

    :param cls: the base ``sloth_ci.bed.Bed`` class
    :param extension: ``{'name': '{extension}', 'config': {param1: value2, param2: value2, ...}}``, extracted from the server config
    '''

    return cls


def extend_cli(cls, extension):
    '''Modify ``sloth_ci.cli.CLI`` to add new ``sci`` commands.

    :param cls: the base ``sloth_ci.cli.CLI`` class
    :param extension: ``{'name': 'spam', 'config': {param1: value2, param2: value2, ...}}``, extracted from the server config
    '''

    return cls


def extend_sloth(cls, extension):
    '''Modify ``sloth_ci.sloth.Sloth`` to change affect app behavior: add loggers, override action executing routine, etc.

    :param cls: the base ``sloth_ci.sloth.Sloth`` class
    :param extension: ``{'name': 'spam', 'config': {param1: value2, param2: value2, ...}}``, extracted from the app config
    '''

    return cls