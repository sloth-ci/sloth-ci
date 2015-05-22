**********
Extensions
**********

Extensions are special modules that add or override the functionality of Sloth CI apps.

For example, the :ref:`file-logs <logs-ext>` extension allows an app to log its activity into a file. The :ref:`ssh-exec <ssh-ext>` extension replaces the default executor with the SSH-based one, allowing the app to execute actions on remote machines.

One app can use multiple extensions, even several ones with the same module (e.g., write logs to several destinations).

Extensions are installed from PyPI with ``pip install sloth-ci.ext.<extension>``.

Sloth CI extensions live in a separate repository at https://bitbucket.org/moigagoo/sloth-ci-extensions/.

When writing your own extensions, refer to the :ref:`dummy extension <dummy-ext>`.

Build Email Notifications
=========================

.. automodule:: sloth_ci.ext.build_email_notifications

.. _docker-ext:

Docker Exec
===========

.. automodule:: sloth_ci.ext.docker_exec

.. _dummy-ext:

Dummy
=====

.. automodule:: sloth_ci.ext.dummy

.. _logs-ext:

File Logs
=========

.. automodule:: sloth_ci.ext.file_logs

OpenVZ Exec
===========

.. automodule:: sloth_ci.ext.openvz_exec

.. _ssh-ext:

SSH Exec
========

.. automodule:: sloth_ci.ext.ssh_exec

Webhooks
========

.. automodule:: sloth_ci.ext.webhooks
