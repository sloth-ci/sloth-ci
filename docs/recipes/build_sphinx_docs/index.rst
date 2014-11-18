*****************
Build Sphinx Docs
*****************

In this recipe, you will see how to build your Sphinx documentation on every push to a particular branch in a repository.

Validator
=========

`github <https://pypi.python.org/pypi/sloth-ci.validators.github>`_ or `bitbucket <https://pypi.python.org/pypi/sloth-ci.validators.bitbucket>`_

.. note:: The example config uses Bitbucket.

Extensions
==========

-   `logs <https://pypi.python.org/pypi/sloth-ci.ext.logs>`_

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

#.  Trigger a build manually with:
    
    .. code-block:: bash
        
        $ sloth-ci trigger docs

    Trigger a build into another directory:

    .. code-block:: bash

        $ sloth-ci trigger docs -p output=/srv/http/