**********
Extensions
**********

**Extensions** add new functionality to Sloth CI server and apps. Extensions change the way an app runs actions, add logging, send emails, new API methods and CLI commands, and much more.

One :doc:`app config <app-config>` can have many extensions; moreover, it can have the same extension used many times. For example, you can use the :mod:`File Logs <sloth_ci.ext.file_logs>` extension to write the error log and use the same extension to write the debug log into a different location.

Server-level extensions are invoked in the :doc:`server config <server-config>`. These extensions change the way Sloth CI server works. For example, the :mod:`Robots.txt <sloth_ci.ext.robots_txt>` extension protects the server from bots; this doesn't affect any particular app but affects the whole server.

Another example of a server-level extension is the Sloth CI API: all web API methods and CLI commands apart from :ref:`cli-start` are implemented in an extension.

A single extension can work on both the app and server levels.

Here is the list of currently available extensions. If you want to create your own extension, refer to the :doc:`developer guide <dev/extension>`.


.. note:: Read the API docs for built-in :ref:`API <apidocs-ext-api>` and :ref:`DB <apidocs-ext-db>` extensions.


Build Email Notifications
=========================

.. automodule:: sloth_ci.ext.build_email_notifications
    :members:


Developer Tools
===============

.. automodule:: sloth_ci.ext.devtools
    :members:


Docker Exec
===========

.. automodule:: sloth_ci.ext.docker_exec
    :members:


File Logs
=========

.. automodule:: sloth_ci.ext.file_logs
    :members:


OpenVZ Exec
===========

.. automodule:: sloth_ci.ext.openvz_exec
    :members:


Robots.txt
==========

.. automodule:: sloth_ci.ext.robots_txt
    :members:


SSH Exec
========

.. automodule:: sloth_ci.ext.ssh_exec
    :members:


Webhooks
========

.. automodule:: sloth_ci.ext.webhooks
    :members:
