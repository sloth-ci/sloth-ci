***********************
Sloth CI: CI for Humans
***********************

.. image:: https://pypip.in/v/sloth-ci/badge.png
    :target: https://pypi.python.org/pypi/sloth-ci/
    :alt: Latest Version

.. image:: https://pypip.in/d/sloth-ci/badge.png
    :target: https://pypi.python.org/pypi/sloth-ci/
    :alt: Downloads

.. image:: https://pypip.in/wheel/sloth-ci/badge.png
    :target: https://pypi.python.org/pypi/sloth-ci/
    :alt: Wheel Status


.. toctree::
    :maxdepth: 2
    :hidden:

    apidocs/index


CI can be a bitch.

Jenkins is nice, but it's Java, thus the memory consumption.

Buildbot is really hairy and weird.

**Sloth CI** is simple. Try it!

.. image:: ../napoleon_sloth.jpg
    :align: center
    :width: 200


Installation
============

Sloth CI can be installed with pip::

    pip install sloth-ci

.. note::

    Sloth CI will work only in Python 3. It *could have been* ported to Python 2 with minimal effort, but the priorities are on the functionality now. Python 3 is better anyway.

This will install the Python package and add the ``sloth-ci`` shell command.

Usage
=====

Use the ``sloth-ci`` command to launch Sloth CI::

    sloth-ci [-h] [--sconfig SCONFIG] [--host HOST] [--port PORT] [--log_dir LOG_DIR] config [config ...]

    positional arguments:
        config             Sloth app config files or dirs.

    optional arguments:
        -h, --help         show help message and exit
        --sconfig SCONFIG  Server config
        --host HOST        Host for the Sloth server (overrides value in sconfig)
        --port PORT        Port for the Sloth server (overrides value in sconfig)
        --log_dir LOG_DIR  Where the log files should be stored (overrides value in sconfig)


.. versionadded:: 0.5.1

The ``config`` param can point either to a file or a directory. In the latter case, all the config files within the directory will be used.

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

    stop_on_first_fail = True

    [provider_data]
    repo = moigagoo/sloth-ci

    [actions]
    echo Got a commit to {branch}

.. versionadded:: 0.3.6

Optional param `stop_on_first_fail` defined if the queue processing should stop on the first fail action execution.

Concept
=======

Here is how this whole thing works:

#.  A *provider* emits a message on some event. For example, a BitBucket repository emits a POST request on every commit.

#.  A *Sloth CI server* is running on you machine. It has one or more *Sloth CI apps* listening to incoming requests. Each app is attached to its own *listener*, which is defined in the app's *config* among other params.

#.  When a request is caught by a listener, it than gets velidated by a *validator*, which is also defined in the app's config.

#.  The validator checks the incoming payload against the *provider data* defined in the app's config. For example, the ``bitbucket`` validator checks whether the payload has come from BitBucket and the repository name is the one we want to listen to.

    A validator can also extract valuable data to be later used during action execution. For example, the ``bitbucket`` validator extracts the ``branch`` name from the incoming payload.

#.  If the payload is validated, the Sloth app proceeds with executing *actions* defined in its config. An action is a single shell command; actions are executed one by one.

Actions can refer to the data extracted on validation. For example, if an app uses the ``bitbucket`` validator, it can use the ``{branch}`` param in its actions.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

