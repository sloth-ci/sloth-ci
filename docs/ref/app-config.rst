.. highlight:: yaml

**********
App Config
**********

**App config** contains the settings for a Sloth CI app:

- unique :ref:`listen point <app-config-listen_point>`
- :ref:`service <app-config-provider>` the triggers actions
- :ref:`actions <app-config-actions>` to run, :ref:`params <app-config-params>` to run them with, and the :ref:`directory <app-config-work_dir>` to run them in
- :ref:`extensions <app-config-extensions>`

.. literalinclude:: _samples/app-config-reference.yml
    :language: yaml

The config is in YAML format. When you create an app with the :ref:`create <cli-create>` command, provide the config as a path to a .yml file:

.. code-block:: bash

    $ sci create /path/to/test.yml

When you create an app :ref:`via the API <api-create>`, provide the config as a URL-encoded string:

.. code-block:: bash

    $ http -f -a login:password localhost:8080 \
            action=create \
            config_string=$(cat test.yml)
    HTTP/1.1 201 Created
    Content-Length: 6
    Content-Type: application/json
    Date: Fri, 27 Nov 2015 21:39:58 GMT
    Server: CherryPy/3.8.0

    "test"


.. _app-config-listen_point:

Listen Point
============

*required*

.. literalinclude:: _samples/app-config-reference.yml
    :lines: 1

Every app has a unique URI called its *listen point*. If the server is running of *example.com:8080*, and the app's listen point is *test*, the full path to the app is *http://example.com:8080/test*.

Listen point can contain slashes. Listen point should *not* start or end with a slash.

.. versionadded:: 2.0.5
    Aliases ``id`` and ``name`` for ``listen_point`` were added.


.. _app-config-provider:

Provider
========

.. literalinclude:: _samples/app-config-reference.yml
    :lines: 3-9

Although you can :ref:`trigger <cli-trigger>` app's actions manually, Sloth CI's true strength is to run actions automatically, e.g. when you push to GitHub.

A service that sends the trigger events is called a *provider*. To work with a certain provider, Sloth CI must have a matching :doc:`validator <../validators>` installed. The ``provider`` param in an app config actually points to the matching *validator*.

:doc:`See available validators and their params → <../validators>`

.. tip:: To make the app triggerable only manually, just skip the whole ``provider`` section.


.. _app-config-actions:

Actions
=======

.. literalinclude:: _samples/app-config-reference.yml
    :lines: 11-13

List of actions to run. Each action is a shell command. Commands are executed one by one top to bottom.

Actions can contain placeholders enclosed between curly brackets: ``{filename}``, ``{branch}``. The placeholders are overriden with values in this order:

#. params from the :ref:`params <app-config-params>` section
#. params extracted by the :doc:`validator <../validators>`
#. params provided with the :ref:`trigger <cli-trigger>` command or via the :ref:`trigger <api-trigger>` API method

Actions can contain stream redirects with ``>`` and ``>>``. Actions can *not* contain context changes like ``cd`` or ``source``.

If you want the whole build to fail when a particular action fails, mark the action with the ``!critical`` tag.

.. versionadded:: 2.0.7
    Actions can be marked critical with the ``!critical`` tag.


.. _app-config-params:

Params
======

.. literalinclude:: _samples/app-config-reference.yml
    :lines: 15-16

Values for the placeholders in :ref:`actions <app-config-actions>`.


.. _app-config-work_dir:

Work Dir
========

.. literalinclude:: _samples/app-config-reference.yml
    :lines: 18

The directory to run the actions in. By default, the actions are executed in the directory you launched Sloth CI in, e.g. ``work_dir="."``.

.. tip:: The ``work_dir`` param is optional, but we highly recommend you to specify it. You want to be 100% sure your ``rm -rf`` runs.


.. _app-config-exec_timeout:

Exec Timeout
============

.. literalinclude:: _samples/app-config-reference.yml
    :lines: 20

The maximal allowed time in seconds for an action to run. If an action takes longer than ``exec_timeout`` seconds to execute, it's terminated.

By default, there's no timeout.


.. _app-config-stop_on_first_fail:

Stop on First Fail
==================

.. deprecated:: 2.0.7
    Use :ref:`!critical <app-config-actions>` instead.

.. literalinclude:: _samples/app-config-reference.yml
    :lines: 22

Stop the build after the first failed action.

Default value: ``false``, i.e. continue with the build even if some actions fail.


.. _app-config-extensions:

Extensions
==========

.. literalinclude:: _samples/app-config-reference.yml
    :lines: 24-29

App-level :doc:`extension <../extensions>` declarations.

A declaration has a unique name (``debug_logs``) and must contain the extension module name (``file_logs``). Depending on the extension, a declaration can include additional params. For example, the mentioned :mod:`File Logs <sloth_ci.ext.file_logs>` extension has eight params.

You can declare the same extension module multiple times under different names::

    extensions:
        debug_logs:
            module: file_logs
            path: /var/log/myapp/
            filename: myapp_debug.log
            level: DEBUG
        info_logs:
            module: file_logs
            path: /var/log/myapp/
            filename: myapp_info.log
            level: INFO

No extensions are declared by default.