*****************
Build Sphinx Docs
*****************

In this recipe, you will see how to build your Sphinx documentation on every push to a particular branch in a repository.

Validator
=========

`github <https://pypi.python.org/pypi/sloth-ci.validators.github>`_ or `bitbucket <https://pypi.python.org/pypi/sloth-ci.validators.bitbucket>`_

Extensions
==========

-   `logs <https://pypi.python.org/pypi/sloth-ci.ext.logs>`_

Config
======

-   :download:`GitHub <docs_github.yml>` 

    .. literalinclude:: docs_github.yml
        :language: yaml

-   :download:`Bitbucket <docs_bitbucket.yml>` 

    .. literalinclude:: docs_bitbucket.yml
        :language: yaml

Steps
=====

#.  In your home directory, create the *projects* directory.

#.  ``cd`` into this directory and clone your repository:

    .. code-block:: bash

        $ git clone https://github.com/username/repository

    or

    .. code-block:: bash

        $ hg clone https://bitbucket.org/username/repository

#.  Create the app from the config file provided:
    
    .. code-block:: bash

        $ sloth-ci create docs_github.yml