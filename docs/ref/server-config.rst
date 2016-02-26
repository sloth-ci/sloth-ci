.. highlight:: yaml

*************
Server Config
*************

**Server config** contains the settings for the Sloth CI server:

- :ref:`host and port <server-config-host-port>` to run on
- :ref:`login and password <server-config-api-auth>` to access the :doc:`API <api>`
- :ref:`paths <server-config-paths>` to the db, logs, and default :doc:`app configs <app-config>`
- :ref:`extensions <server-config-extensions>`
- :ref:`daemon status <server-config-daemon>`

.. literalinclude:: _samples/server-config-reference.yml
    :language: yaml

By default, Sloth CI tries to use a file called *sloth.yml* in the current directory as a server config, but you can specify a custom one with the :doc:`-c <cli>` param:

    .. code-block:: bash

        $ sci -c /path/to/myconfig.yml start


.. _server-config-host-port:

Host, Port
==========

*required*

.. literalinclude:: _samples/server-config-reference.yml
    :lines: 1-2

The host and port for the Sloth CI server to run on.

.. tip:: To make the server accessible from the Internet, set ``host`` to ``0.0.0.0``.


.. _server-config-api-auth:

API Access Credentials
======================

*required*

.. literalinclude:: _samples/server-config-reference.yml
    :lines: 4-6

Login and password to access the :doc:`Sloth CI API <api>`.

.. versionchanged:: 2.0.4
    Alias ``auth`` for ``api_auth`` was added.


.. _server-config-paths:

Paths
=====

.. literalinclude:: _samples/server-config-reference.yml
    :lines: 8-15

.. tip:: Use absolute paths. Relative paths work too, but absolute ones are more reliable.

access_log
    Path to the log that records all incoming requests.

    Default value: ``sloth_access.log``

error_log
    Path to the log that records app creation and extension loading errors, server startup and tier down info.

    Default value: ``sloth_error.log``

db
    Path to the SQLite DB file to store the app logs in.

    Default value: ``sloth.db``

configs
    List of paths to the :doc:`app configs <app-config>` to load on server startup.

    Items can be file paths or glob patterns::

        configs:
            - /path/to/app.yaml
            - /path/to/configs/*.yml

    No app configs are loaded by default.


.. _server-config-extensions:

Extensions
==========

.. literalinclude:: _samples/server-config-reference.yml
    :lines: 17-19

Server-level :doc:`extension <../extensions>` declarations.

A declaration has a unique name (``hide-from-robots``) and must contain the extension module name (``robots_txt``). Depending on the extension, a declaration can include additional params. For example, the mentioned :mod:`Robots.txt <sloth_ci.ext.robots_txt>` extension has two optional params: ``file`` and ``path``.

You can declare the same extension module multiple times under different names::

    extensions:
        hide-from-robots:
            module: robots_txt
        robots-txt-on-a-different-path:
            module: robots_txt
            path: /static/robots.txt

No extensions are declared by default.

.. note:: The built-in API extension is silently loaded without declaration.


.. _server-config-daemon:

Daemon
======

.. literalinclude:: _samples/server-config-reference.yml
    :lines: 21

Run Sloth CI as a daemon. Default is ``false``.

.. important:: This params works only in UNIX-based systems. If you launch Sloth CI with ``daemon: true`` on Windows, it will crash.
