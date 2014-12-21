********************************************
Execute Actions on Multiple Machines via SSH
********************************************

This recipe shows how to use the SSH executor to run the same actions across multiple machines.

Our app will connect to three remote hosts with the keys it finds in a specified directory and perform certain actions.

Validator
=========

`github <https://pypi.python.org/pypi/sloth-ci.validators.github>`_ or `bitbucket <https://pypi.python.org/pypi/sloth-ci.validators.bitbucket>`_

.. note:: The example config uses Bitbucket.

Extensions
==========

-   `file_logs <https://pypi.python.org/pypi/sloth-ci.ext.file-logs>`_
-   `ssh_exec <https://pypi.python.org/pypi/sloth-ci.ext.ssh-exec>`_

Config
======

-   :download:`Download <ssh.yml>` 

    .. literalinclude:: ssh.yml
        :language: yaml

Steps
=====

#.  Create the app from the config file provided:
    
    .. code-block:: bash

        $ sloth-ci create /path/to/ssh.yml

#.  Trigger the actions with:
    
    .. code-block:: bash
        
        $ sloth-ci trigger ssh