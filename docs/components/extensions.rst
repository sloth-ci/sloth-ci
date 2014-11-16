**********
Extensions
**********

Extensions are special modules that add or override the functionality of Sloth CI :doc:`apps <apps>`.

For example, the ``logs`` extension allows an app to log its activity into a file. The ``ssh_exec`` extension replaces the default executor with the SSH-based one, allowing the app to execute actions on remote machines.

One app can use multiple extensions, even several ones with the same module (e.g., write logs to several destinations).

Extensions are installed from PyPI with ``pip install sloth-ci.ext.<extension>``.

Sloth CI extensions live in a separate repository at https://bitbucket.org/moigagoo/sloth-ci-extensions/.