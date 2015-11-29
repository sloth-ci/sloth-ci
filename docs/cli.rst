.. highlight:: bash

***
CLI
***

Sloth CI ships with the ``sci`` [#sci-alias]_ command line utility that lets you control the server and apps with a variety of :ref:`commands <cli-commands>`::

    $ sci COMMAND [OPTIONS] [PARAMS] ...

Some commands have options, prefixed with a dash: ``-config``, ``-level``. You can shorten option names up to a single character: ``-c``, ``-l``; just make sure your abbreviations are unambiguous [#ambiguous-options]_.

Here are the options of the ``sci`` command itself:

``-config CONFIG``
    Define path to the :doc:`server config <server-config>` file::

        # Start Sloth CI with a custom config:
        $ sci -c path/to/custom_config.yml start

``-h, --help``
    Show help. Use ``-h`` after any command to see its help message.

``-version``
    Show the version of the locally installed Sloth CI [#local-version]_.


.. _cli-commands:

Commands
========

Here're the built-in commands. If they are not enough, feel free to :ref:`add your own <dev-extension-cli>`.

.. _cli-start:

start
-----

Start the Sloth CI server::

    $ sci start
    Starting Sloth CI on http://localhost:8080


.. _cli-stop:

stop
----

Stop the Sloth CI server::

    $ sci stop
    Stopping Sloth CI on http://localhost:8080


.. _cli-restart:

restart
-------

Restart, i.e. :ref:`stop <cli-stop>` then :ref:`start <cli-start>`, the Sloth CI server::

    $ sci restart
    Restarting Sloth CI on http://localhost:8080


.. _cli-status:

status
------

*Aliases:* ``stat``, ``st``

Get the status—running ir not running—and version of the Sloth CI server::

    $ sci st
    Sloth CI version 2.0.1 is running on http://localhost:8080


.. _cli-create:

create
------

*Alias:* ``add``

Create a Sloth CI app from the given config file and :ref:`api-bind` them::

    $ sci add myapp.yml
    App "myapp" created
    App "myapp" bound with config file "myapp.yml"


.. _cli-history:

history
-------

*Aliases:* ``hist``, ``builds``

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

::

    $ sci hist -l 10 -p 2 myapp
    Timestamp                 Status
    ------------------------  ------------------------------
    Mon Nov  2 21:47:10 2015  Completed 2/2
    Mon Nov  2 21:47:05 2015  Triggered, actions in queue: 2


.. _cli-info:

info
----

Show the config file bound with the app and its latest build status::

    $ sci info myapp
    Config File    Last Build Message    Last Build Timestamp
    ------------  --------------------  -------------------------
    myapp.yml      Completed 2/2         Mon Nov  2 21:47:10 2015


.. _cli-list:

list
----

*Alias:* ``ls``

List all available apps' listen points::

    $ sci ls
    myapp
    myotherapp


.. _cli-logs:

logs
----

*Alias:* ``lg``

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

::

    $ sci lg -p 3 myapp
    Timestamp                 Message
    ------------------------  --------------------------------
    Mon Nov  2 21:21:58 2015  Bound with config file myapp.yml
    Mon Nov  2 21:21:58 2015  Listening on test
    Mon Nov  2 21:13:32 2015  Stopped


.. _cli-reload:

reload
------

*Aliases:* ``update``, ``up``

Recreate the app from the bound config file. Invoke after changing the app config to apply the changes.

Reload is a shortcut for :ref:`remove <cli-remove>` and :ref:`create <cli-create>`::

    $ sci up myapp
    App "myapp" removed
    App "myapp" created
    App "myapp" bound with config file "myapp.yml"


.. _cli-remove:

remove
------

*Aliases:* ``del``, ``rm``

Remove an app::

    $ sci rm myapp
    App "myapp" removed


.. _cli-trigger:

trigger
-------

*Aliases:* ``run``, ``fire``

Trigger the app to run its actions. If the app doesn't use a provider, this is the only way to run its actions.

``-wait``
    Block and wait for the build to finish.

``-params param1=value1 param2=value2 ...``
    List of params in the form ``param=value`` to be used in the actions.

    If the app's actions use params extracted from incoming payload, you must provide the necessary param replacements.

::

    $ sci run myapp -p foo=bar
    Actions triggered on test


.. rubric:: Footnotes

.. [#sci-alias] When you install Sloth CI, two commands are added to your system: ``sloth-ci`` and ``sci``. They are identical, and you can use any one you like. We use ``sci`` everywhere in the docs for brevity.

.. [#ambiguous-options] All options on this page can be safely called by a single character; no default subcommand has two options starting with the same character. However, extensions can add there own options, which can be ambiguous.

.. [#local-version] ``sci -v`` shows the version of Sloth CI installed on your machine, i.e. the client, not the version of the server you're connecting to. To know the Sloth CI version on a remote machine, use :ref:`sci status <cli-status>`.
