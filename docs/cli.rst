***
CLI
***

Here's the output of the ``sloth-ci --help`` command:

.. code-block:: bash

    Sloth CI.

    Usage:
      sloth-ci start | restart | stop [-c <file>]
      sloth-ci create <config_source> [-c <file>]
      sloth-ci remove <listen_point> [-c <file>]
      sloth-ci trigger <listen_point> [-p <params>] [-c <file>]
      sloth-ci --version
      sloth-ci -h

    Options:
      -c <file>, --config <file>    Path to the server config file [default: ./sloth.yml]
      -p --params <params>          Params to trigger the actions with. String like 'param1=val1,param2=val2'
      -h --help                     Show this screen
      -v --version                  Show version

By default, Sloth CI will attempt to find the file *sloth.yml* in the directory it was called in and use it as its server config. You can specify your own config file path as the optional ``-c`` (or ``--config``) argument.

.. hint::

    The ``start`` command utilizes all of the config content to set up the server, whereas the other commands only need the ``host``, ``port``, and ``api_auth`` values to connect to an existing server. This means that you can use a simpler config to control a server, and you can have many of them to control multiple Sloth CI servers.

``start``
=========

Start a Sloth CI server with a particular configuration. The configuration is specified in the :ref:`server config file <server-config>`.

``restart``
===========

Ask a Sloth CI server to restart.

.. important::

    This command only *asks* for a restart, it can't guarantee that the server will restart immediatelly or ever at all. You should check the restart success in the server's logs.

``stop``
========

Ask a Sloth CI server to stop.

.. important::

    This command only *asks* for a stop, it can't guarantee that the server will stop immediatelly or ever at all. You should check the stop success in the server's logs.

``create``
==========

Create a Sloth CI app with a paricular configuration. The configuration is specified either as a path to a YAML file or as a string. Refer to the :ref:`app config <app-config>` description.

The new app's listen point is returned if the creation was successful.

``remove``
==========

Remove a Sloth CI app on a particular listen point.

``trigger``
===========

Trigger the app's actions execution with a particular set of params.

.. important::
    
    This command *triggers*, not *executes* the actions. Its call is considered successful it the action execution was successfully trigerred, not necessarily if all the action were successfully executed. You should check the execution success in the app's logs.

In the ``-p`` (or ``--params``) argument, you must specify the params that are usually extracted from the incoming payload. You can also override the values from the ``params`` section of the :ref:`app config <app-config>`.

.. note::

    Normally, while executing the actions, Sloth CI uses the params from the ``params`` section in the apps's config and the params extracted from the incoming payload.
    
    In case of a forced execution, there is no payload, thus, no params. In the face of ambiguity, Sloth CI refuses the temptation to guess, so you must specify the params explicitly.