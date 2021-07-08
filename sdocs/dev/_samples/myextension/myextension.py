"""Describe your extension.


Installation
------------

.. code-block:: bash

    $ pip install sloth-ci.ext.myextension


Usage
-----

.. code-block:: yaml
    :caption: myextension.yml

    extensions:
        myextension:
            # Use the module sloth_ci.ext.myextension.
            module: myextension
            param1: value1
            param2: value2
            ...
"""

__title__ = "sloth-ci.ext.myextension"
__description__ = "Describe your extension"
__version__ = "0.0.1"
__author__ = "Your Name"
__author_email__ = "your@email.com"
__license__ = "MIT"


def extend_bed(cls, extension):
    """Modify ``sloth_ci.bed.Bed`` to add API endpoints and custom URI handlers.

    :param cls: the base ``sloth_ci.bed.Bed`` class
    :param extension: ``{'name': '{extension}', 'config': {param1: value2, param2: value2, ...}}``, extracted from the server config
    """

    class Bed(cls):
        pass

    return Bed


def extend_cli(cls, extension):
    """Modify ``sloth_ci.cli.CLI`` to add new ``sci`` commands.

    :param cls: the base ``sloth_ci.cli.CLI`` class
    :param extension: ``{'name': 'myextension', 'config': {param1: value2, param2: value2, ...}}``, extracted from the server config
    """

    class CLI(cls):
        pass

    return CLI


def extend_sloth(cls, extension):
    """Modify ``sloth_ci.sloth.Sloth`` to affect app behavior: add loggers, override action executing routine, etc.

    :param cls: the base ``sloth_ci.sloth.Sloth`` class
    :param extension: ``{'name': 'myextension', 'config': {param1: value2, param2: value2, ...}}``, extracted from the app config
    """

    class Sloth(cls):
        pass

    return Sloth
