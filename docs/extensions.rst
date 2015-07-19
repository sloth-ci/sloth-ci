**********
Extensions
**********

Extensions add or override Sloth CI's functionality.

All extensions live in a separate repository at https://bitbucket.org/moigagoo/sloth-ci-extensions/ and are installed from PyPI with ``pip install sloth-ci.ext.<extension>``.

There're 2 types of extensions:

    -   app extensions
    -   server extensions

App Extensions
==============

App extension is enabled for a particular app and deals only with its workflow. One app can have multiple extensions, even multiple invokations of the same extension.

App extensions extend or override app's default workflow:

    -   :ref:`file-logs <file-logs-ext>` extension lets the app write logs into a file
    -   :ref:`ssh-exec <ssh-exec-ext>` extension replaces the default executor and executes actions on remote machines via SSH

App extensions are declared in the ``extensions`` section of an :doc:`app config <configs/apps>`.

App extensions override the class :class:`sloth_ci.sloth.Sloth` one after another, so that the resulting class has all the features from all enabled extensions. Refer to the :ref:`dummy app extension <dummy-app-ext>` when developing your own app extensions.

Build Email Notifications
-------------------------

.. automodule:: sloth_ci.ext.build_email_notifications

.. _docker-ext:

Docker Exec
-----------

.. automodule:: sloth_ci.ext.docker_exec

.. _dummy-app-ext:

Dummy App
---------

.. automodule:: sloth_ci.ext.dummy_app

.. _file-logs-ext:

File Logs
---------

.. automodule:: sloth_ci.ext.file_logs

OpenVZ Exec
-----------

.. automodule:: sloth_ci.ext.openvz_exec

.. _ssh-exec-ext:

SSH Exec
--------

.. automodule:: sloth_ci.ext.ssh_exec

Webhooks
--------

.. automodule:: sloth_ci.ext.webhooks

Server Extensions
=================

Server extension is enabled for the whole Sloth CI server and deals with stuff not related to any particular app. The server can have multiple extensions, even multiple invokations of the same extension.

Server extensions deal with server configuration, routing, and app management:

    -   :ref:`robots-txt <robots-txt-ext>` add a route for the robots.txt file and serves the file on this route

Server extensions are declared in the ``extensions`` section of an :doc:`server config <configs/server>`.

Server extensions override the class :class:`sloth_ci.bed.Bed` one after another, so that the resulting class has all the features from all enabled extensions. Refer to the :ref:`dummy server extension <dummy-server-ext>` when developing your own app extensions.

.. _dummy-server-ext:

Dummy Server
------------

.. automodule:: sloth_ci.ext.dummy_server

.. _robots-txt-ext:

Robots.txt
----------

.. automodule:: sloth_ci.ext.robots_txt