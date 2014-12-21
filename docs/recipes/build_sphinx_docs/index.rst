*****************
Build Sphinx Docs
*****************

In this recipe, you will see how to build your Sphinx documentation on every push to a particular branch in a repository.

It is assumed that a Sloth CI server is already running on localhost:8080.

Validator
=========

`github <https://pypi.python.org/pypi/sloth-ci.validators.github>`_ or `bitbucket <https://pypi.python.org/pypi/sloth-ci.validators.bitbucket>`_

.. note:: The example config uses Bitbucket.

Extensions
==========

-   `file_logs <https://pypi.python.org/pypi/sloth-ci.ext.file-logs>`_

Config
======

-   :download:`Download <docs.yml>` 

    .. literalinclude:: docs.yml
        :language: yaml

Steps
=====

#.  In your home directory, create the *projects* directory.

#.  Create the app from the config file provided:

    .. code-block:: bash

        $ sloth-ci create /path/to/docs.yml

#.  Trigger a build manually with this CLI command:

    .. code-block:: bash

        $ sloth-ci trigger docs

    or by opening this URL in your browser::

        http://localhost:8080/?action=trigger&listen_point=docs


    .. hint::

        Trigger a build into another directory:

        .. code-block:: bash

            $ sloth-ci trigger docs -p output=/srv/http/

        or::

            http://localhost:8080/?action=trigger&listen_point=docs&output=%2Fsrv%2Fhttp%2F