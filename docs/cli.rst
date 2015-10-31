********
Commands
********

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

``-version``
    Show the version of the locally installed Sloth CI [#local-version]_.


.. _cli-sci-start:

``sci start``
=============

Start


.. _cli-sci-create:

``sci create``
==============

Create


.. _cli-sci-logs:

``sci logs``
============

Logs


.. _cli-sci-reload:

``sci reload``
==============

Reload


.. _cli-sci-status:

``sci status``
==============

Status

.. rubric:: Footnotes

.. [#sci-alias] When you install Sloth CI, two commands are added to your system: ``sloth-ci`` and ``sci``. They are identical, and you can use any one you like. We use ``sci`` everywhere in the docs for brevity.

.. [#ambiguous-options] All options on this page can be safely called by a single character; no default subcommand has two options starting with the same character. However, extensions can add there own options, which can be ambiguous.

.. [#local-version] ``sci -version`` shows the version of Sloth CI that is installed on your machine, not the one specified in the server config. To know the version of Sloth CI installed on a remote machine, use :ref:`sci status <cli-sci-status>`.