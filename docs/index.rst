***********************
Sloth CI: CI for Humans
***********************

.. image:: https://pypip.in/version/sloth-ci/badge.svg?style=flat
    :target: https://pypi.python.org/pypi/sloth-ci/
    :alt: Latest Version

.. image:: https://pypip.in/download/sloth-ci/badge.svg?style=flat
    :target: https://pypi.python.org/pypi/sloth-ci/
    :alt: Downloads

.. image:: https://pypip.in/wheel/sloth-ci/badge.svg?style=flat
    :target: https://pypi.python.org/pypi/sloth-ci/
    :alt: Wheel Status

.. image:: https://pypip.in/status/sloth-ci/badge.svg?style=flat
    :target: https://pypi.python.org/pypi/sloth-ci/
    :alt: Development Status

.. toctree::
    :maxdepth: 2
    :hidden:

    examples

Sloth CI is an easy-to-use, lightweight, extendible tool that does whatever you tell it to when a certain things happens.

.. image:: ../napoleon_sloth.jpg
    :align: center
    :width: 200


Requirements
============

Sloth CI runs with Python 3 on Windows, Linux, and (supposedly) Mac.

Installation
============

Install Sloth CI with pip::

    pip install sloth-ci


This will install the Python package and the ``sloth-ci`` shell command.

It will also copy the default server config to the path depending on your system:

    -   *$HOME\\AppData\\Local\\sloth-ci\\configs* for Windows
    -   */etc/sloth-ci/configs* for Linux

Usage
=====

Use the ``sloth-ci`` command to launch Sloth CI::

    usage: sloth-ci [-h] [-s SCONFIG] [-H HOST] [-p PORT] [-l LOG_DIR] [-d] [config [config ...]]

    positional arguments:
      config                Sloth app config files or dirs.

    optional arguments:
      -h, --help            show this help message and exit
      -s SCONFIG, --sconfig SCONFIG
                            Server config.
      -H HOST, --host HOST  Host for the Sloth server (overrides value in
                            sconfig).
      -p PORT, --port PORT  Port for the Sloth server (overrides value in
                            sconfig).
      -l LOG_DIR, --log_dir LOG_DIR
                            Where the log files should be stored (overrides value
                            in sconfig).
      -d, --daemon          Run as daemon.

Most of these params you don't need. For example, if you're on Linux, you can just launch Sloth CI with ``sloth-ci -d``. The server config will be taken from the */etc/sloth-ci/configs/server.conf* file, and you can just put the app configs in */etc/sloth-ci/configs/apps*—Sloth CI will add new apps on the fly.

By default, the logs are stored in */var/logs/sloth-ci* on Linux and in *$HOME\\AppData\\sloth-ci\\logs* on Windows.

You can override all default params explicitly when calling the script.

See some examples of hopw you can use Sloth CI on :doc:`this page <examples>`.

.. versionadded:: 0.5.1

The ``config`` param can point either to a file or a directory. In the latter case, all the config files within the directory will be used.

Minimal Server Config
---------------------

::

    host = 0.0.0.0
    port = 8080

Minimal App Config
------------------

::

    provider = bitbucket

    [provider_data]
    repo = moigagoo/sloth-ci

    [actions]
    echo Got a commit to {branch}
    echo {foo}

.. versionadded:: 0.3.6

Optional param `stop_on_first_fail` defined if the queue processing should stop on the first fail action execution.

.. versionadded:: 0.5.8

The `params` section added.

Extensions And Validators
-------------------------

Sloth CI per se implements only the basic thing—it just runs the actions on the machine it is laucnhed on. No logging or remote execution. Strictly speaking, raw Sloth CI can't do anything, because it doesn't know what to listen to.

So, here come **validators**. There're currently three public validators: *github*, *bitbucket*, and *dummy*. They correspond to, respectively, GitHub commit hooks, Bitbucket commit hooks, and a simple GET request with the ``message`` param. Validators live in a `separate repo <http://bitbucket.org/moigagoo/sloth-ci-validators>`_.

What a validator does is:
    -   checks the payload origin (e.g. whether it's really from GitHub and not from a hacker)
    -   checks if it's the expected payload (e.g. from the repo we're interested in)
    -   extracts valueable data, like branch name

Only after the validator makes sure the payload is correct (i.e. *validates* it), the actions are executed.

And the way they are executed is specified by **extensions**. For example, if you want to enable logging to a file and run the actions via SSH on a bunch of remote servers, you'd use the *logs* and *ssh-exec* extensions. Extensions, like validators, have `their own home <http://bitbucket.org/moigagoo/sloth-ci-extensions>`_.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`