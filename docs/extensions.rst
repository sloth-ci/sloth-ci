**********
Extensions
**********

**Extensions** add new functionality to Sloth CI server and apps. Extensions change the way an app runs actions, add logging, send emails, new API methods and CLI commands, and much more.

One :doc:`app config <app-config>` can have many extensions; moreover, it can have the same extension used many times. For example, you can use the :ref:`File Logs <ext-file-logs>` extension to write the error log and use the same extension to write the debug log into a different location.

Server-level extensions are invoked in the :doc:`server config <server-config>`. These extensions change the way Sloth CI server works. For example, the :ref:`Robots.txt <ext-robots-txt>` extension protects the server from bots; this doesn't affect any particular app but affects the whole server.

Another example of a server-level extension is the :doc:`Sloth CI API <api>`. Basic API has only the :ref:`start <api-start>` method; the rest if the methods are supplied by the API extension.

A single extension can work on the app and server level.

Here is the list of currently available extensions. If you want to create your own extension, refer to the :doc:`developer guide <dev/extension>`.


.. _ext-build-email-notifications:

Build Email Notifications
=========================

.. automodule:: sloth_ci.ext.build_email_notifications
    :members:


.. _ext-docker-exec:

Docker Exec
===========

.. automodule:: sloth_ci.ext.docker_exec
    :members:


.. _ext-file-logs:

File Logs
=========

.. automodule:: sloth_ci.ext.file_logs
    :members:


.. _ext-openvz-exec:

OpenVZ Exec
===========

.. automodule:: sloth_ci.ext.openvz_exec
    :members:


.. _ext-robots-txt:

Robots.txt
==========

.. automodule:: sloth_ci.ext.robots_txt
    :members:


.. _ext-ssh-exec:

SSH Exec
========

.. automodule:: sloth_ci.ext.ssh_exec
    :members:


.. _ext-webhooks:

Webhooks
========

.. automodule:: sloth_ci.ext.webhooks
    :members: