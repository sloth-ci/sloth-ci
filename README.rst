********
Sloth CI
********

.. image:: https://pypip.in/v/sloth-ci/badge.png
    :target: https://pypi.python.org/pypi/sloth-ci/
    :alt: Latest Version

.. image:: https://pypip.in/d/sloth-ci/badge.png
    :target: https://pypi.python.org/pypi/sloth-ci/
    :alt: Downloads

.. image:: https://pypip.in/wheel/sloth-ci/badge.png
    :target: https://pypi.python.org/pypi/sloth-ci/
    :alt: Wheel Status

CI can be a bitch.

Jenkins is nice, but it's Java, thus the memory consumption.

Buildbot is really hairy and weird.

**Sloth CI** is simple. Try it!

.. image:: https://dl.dropbox.com/u/43859367/napoleon_sloth.jpg
    :align: center
    :width: 200

Installation
============

Sloth CI can be installed with pip::

    pip install sloth-ci

.. note::

    Sloth CI will work only in Python 3. It *could have been* ported to Python 2 with minimal effort, but the priorities are on the functionality now. Python 3 is better anyway.

This will install the Python package and add the ``sloth-ci`` shell command.

The repo is at `bitbucket.org/moigagoo/sloth-ci <https://bitbucket.org/moigagoo/sloth-ci>`_.

Read the full documentation at `sloth-ci.rtfd.org <http://sloth-ci.rtfd.org>`_

Install provider(s)
===================

Sloth CI listens to payload from *providers* to trigger your actions.

Invcoming payload form a particular provider is valiadated by the respective *validator*.

Validators can be installed with pip::

    pip install sloth-ci.validators.bitbucket

...or::

    pip install sloth-ci.validators.github

...or roll-your-own with::

    pip install sloth-ci.validators.dummy

Validators are maintained in a separate repo at  https://bitbucket.org/moigagoo/sloth-ci-validators.

Install app extensions
======================

Additional functions like logging to a file and non-default executors are available via *extensions*.

Extensions are installed via pip::

	pip install sloth-ci.ext.logs

Dummy extension  (just like the Dummy validator) can be referred to while developing your own extensions::

	pip install sloth-ci.ext.dummy

Extensions are maintained in a separate repo at  https://bitbucket.org/moigagoo/sloth-ci-extensions.

Usage
=====

Use the ``sloth-ci`` command to launch Sloth CI::

    sloth-ci [-h] [--sconfig SCONFIG] [--host HOST] [--port PORT] [--log_dir LOG_DIR] config [config ...]

    positional arguments:
        config             Sloth app config(s); config per app.

    optional arguments:
        -h, --help         show help message and exit
        --sconfig SCONFIG  Server config
        --host HOST        Host for the Sloth server (overrides value in sconfig)
        --port PORT        Port for the Sloth server (overrides value in sconfig)
        --log_dir LOG_DIR  Where the log files should be stored (overrides value in sconfig)

Server Config Example
---------------------

::

    host = 0.0.0.0
    port = 8080
    log_dir = /var/log/sloth/

Sloth App Config Example
------------------------

::

    listen_to = /sloth-listener

    work_dir = /home/sloth/my_project

    provider = bitbucket

    [provider_data]
    repo = moigagoo/sloth-ci

    [params]
    foo = bar

    [actions]
    echo Got a commit to {branch}
    echo {foo}
