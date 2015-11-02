************
CLI Commands
************

Sloth CI ships with the ``sci`` command that lets you control the server and apps with a variaty of subcommands [#sci-alias]_.

Most subcommands have options prefixed with a dash, e.g. ``-config`` and ``-level``. Options can be abbreviated up to a single character, e.g. ``-c`` and ``-l``; just make sure the abbreviation is not ambiguous [#ambiguous-options]_.

If you feel that these commands are not enough, extend the CLI with your own commands, as described in the :ref:`developer guide <dev-extension-cli>`.


.. _cli-sci:

``sci``
=======

.. code-block:: bash

    $ {sci, sloth-ci} [-config CONFIG] [-h, --help] [-version] {subcommand}

The command itself doesn't do anything, but combined with the ``-config`` flag it lets you pick the config file for any subcommand. If the config is not defined explictly, ``sci`` looks for *sloth.yml* in the directory it was invoked in.

``-config CONFIG``
    Define path to the :doc:`server config <server-config>` file.

    .. code-block:: bash

        # Start Sloth CI with a custom config:
        $ sci -c path/to/custom_config.yml start

``-h, --help``
    Show help. If you invoke ``sci`` without any subcommand or options, it also shows help.

    Every subcommand has this flag.

``-version``
    Show the version of the locally installed Sloth CI [#local-version]_.


.. _cli-sci-start:

``sci start``
=============

Start the Sloth CI server.

.. code-block:: bash

    $ sci start
    Starting Sloth CI on http://localhost:8080


.. _cli-sci-stop:

``sci stop``
============

Stop the Sloth CI server.

.. code-block:: bash

    $ sci stop
    Stopping Sloth CI on http://localhost:8080


.. _cli-sci-restart:

``sci restart``
===============

Restart, i.e. :ref:`stop <cli-sci-stop>` then :ref:`start <cli-sci-start>`, the Sloth CI server.

.. code-block:: bash

    $ sci restart
    Restarting Sloth CI on http://localhost:8080


.. _cli-sci-status:

``sci status (stat, st)``
=========================

Get the status—running ir not running—and version of the Sloth CI server.

.. code-block:: bash

    $ sci st
    Sloth CI version 2.0.1 is running on http://localhost:8080


.. _cli-sci-create:

``sci create (add)``
====================

Create a Sloth CI app from the given config file and :ref:`api-bind` them.

.. code-block:: bash

    $ sci add myapp.yml
    App "myapp" created
    App "myapp" bound with config file "myapp.yml"


.. _cli-sci-history:

``sci history (hist, builds)``
==============================

View paginated app build history.

``-level LEVEL``
    Minimal log level to show:

    40
        ERROR, failed builds.

    30
        WARNING, partially completed builds.

    20 (default)
        INFO, completed builds.

    10
        DEBUG, trigger events.

``-from-page FROM_PAGE``
    Pagination starting page. Enumeration start with 1; ``-f 1`` means the latest page.

``-to-page TO_PAGE``
    Pagination ending page.

``-per-page PER_PAGE``
    Number of log records per page.

``-verbose``
    Show the *Level* column.

.. code-block:: bash

    $ sci hist -l 10 -p 2 myapp
    Timestamp                 Status
    ------------------------  ------------------------------
    Mon Nov  2 21:47:10 2015  Completed 2/2
    Mon Nov  2 21:47:05 2015  Triggered, actions in queue: 2


.. _cli-sci-info:

``sci info``
============

Show the config file bound with the app and its latest build status.

.. code-block:: bash

    $ sci info myapp
    Config File    Last Build Message    Last Build Timestamp
    ------------  --------------------  -------------------------
    myapp.yml      Completed 2/2         Mon Nov  2 21:47:10 2015


.. _cli-sci-list:

``sci list (ls)``
=================

List all available apps' listen points.

.. code-block:: bash

    $ sci ls
    myapp
    myotherapp


.. _cli-sci-logs:

``sci logs (lg)``
=================

View paginated app logs.

``-level LEVEL``
    Minimal log level to show:

    50
        CRITICAL, errors that don't allow apps to be created, e.g missing validator.

    40
        ERROR, missing extension and failed builds.

    30
        WARNING, partially completed builds.

    20 (default)
        INFO, completed builds.

    10
        DEBUG, stdout and stderr.

``-from-page FROM_PAGE``
    Pagination starting page. Enumeration start with 1; ``-f 1`` means the latest page.

``-to-page TO_PAGE``
    Pagination ending page.

``-per-page PER_PAGE``
    Number of log records per page.

``-verbose``
    Show the *Level* column.

.. code-block:: bash

    $ sci lg -p 3 myapp
    Timestamp                 Message
    ------------------------  --------------------------------
    Mon Nov  2 21:21:58 2015  Bound with config file myapp.yml
    Mon Nov  2 21:21:58 2015  Listening on test
    Mon Nov  2 21:13:32 2015  Stopped


.. _cli-sci-reload:

``sci reload (update, up)``
===========================

Recreate the app from the bound config file. Invoke after changing the app config to apply the changes.

Reload is a shortcut for :ref:`remove <cli-sci-remove>` and :ref:`create <cli-sci-create>`.

.. code-block:: bash

    $ sci up myapp
    App "myapp" removed
    App "myapp" created
    App "myapp" bound with config file "myapp.yml"


.. _cli-sci-remove:

``sci remove (del, rm)``
========================

Remove an app.

.. code-block:: bash

    $ sci rm myapp
    App "myapp" removed


.. _cli-sci-trigger:

``sci trigger (run, fire)``
===========================

Trigger the app to run its actions. If the app doesn't use a provider, this is the only way to run its actions.

``-wait``
    Block and wait for the build to finish.

``-params [PARAMS [PARAMS ...]]``
    List of params in the form ``param=value`` to be used in the actions.

    If the app's actions use params extracted from incoming payload, you must provide the necessary param replacements.

.. code-block:: bash

    $ sci run myapp -p foo=bar
    Actions triggered on test


.. rubric:: Footnotes

.. [#sci-alias] When you install Sloth CI, two commands are added to your system: ``sloth-ci`` and ``sci``. They are identical, and you can use any one you like. We use ``sci`` everywhere in the docs for brevity.

.. [#ambiguous-options] All options on this page can be safely called by a single character; no default subcommand has two options starting with the same character. However, extensions can add there own options, which can be ambiguous.

.. [#local-version] ``sci -version`` shows the version of Sloth CI that is installed on your machine, not the one specified in the server config. To know the version of Sloth CI installed on a remote machine, use :ref:`sci status <cli-sci-status>`.
