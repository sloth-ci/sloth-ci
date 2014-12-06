***********************
Sloth CI: CI for Humans
***********************

.. image:: https://pypip.in/version/sloth-ci/badge.svg
    :target: https://pypi.python.org/pypi/sloth-ci/
    :alt: Latest Version

.. image:: https://pypip.in/download/sloth-ci/badge.svg
    :target: https://pypi.python.org/pypi/sloth-ci/
    :alt: Downloads

.. image:: https://pypip.in/py_versions/sloth-ci/badge.svg
    :target: https://pypi.python.org/pypi/sloth-ci/
    :alt: Supported Python Versions

.. image:: https://pypip.in/wheel/sloth-ci/badge.svg
    :target: https://pypi.python.org/pypi/sloth-ci/
    :alt: Wheel Status

.. image:: https://pypip.in/status/sloth-ci/badge.svg
    :target: https://pypi.python.org/pypi/sloth-ci/
    :alt: Development Status

Sloth CI is an easy-to-use, lightweight, extendable tool that executes actions you need when certain events happen.

Sloth CI was created because Jenkins is too heavy and Buildbot was too hard to learn.

Read the docs at http://sloth-ci.cloudapp.net/ (yes, they are built with Sloth CI).

Requirements
============

Sloth CI runs with Python 3 on Windows, Linux, and Mac.

Install
=======

Install Sloth CI, the Bitbucket validator, and the logs extension with pip:

.. code-block:: bash

    $ pip install sloth-ci sloth-ci.validators.bitbucket sloth-ci.ext.logs

Configure
=========

Create a file named *sloth.yml* in any directory and cd to that directory.

Here's how your sloth.yml can look like:

.. code-block:: yaml

    host: 0.0.0.0
    
    port: 8080
    
    daemon: true
    
    log_dir: /var/log/sloth-ci

    api_auth:
        login: admin
        password: supersecret

Start
=====

Start the Sloth CI server with:

.. code-block:: bash

   $ sloth-ci start

Create App
==========

Create a file called like *myapp.yml*:

.. code-block:: yaml

    listen_point: docs

    work_dir: ~/projects

    provider:
        bitbucket:
            repo: username/repository

    extensions:
        logs:
            module: logs
            path: /var/log/sloth-ci
            filename: docs_errors.log
            level: ERROR

    actions:
        - rm -rf repository
        - hg clone https://bitbucket.org/username/repository
        - hg up {branch} --cwd repository
        - pip3 install -U sphinx
        - pip3 install -r repository/docs/requirements.txt
        - sphinx-build -aE repository/docs/ {output}/{branch}

    params:
        output: /var/www/html

Create the app from the config:

.. code-block:: bash

    $ sloth-ci create /path/to/myapp.yml
    App created, listening on docs

.. note:: Run ``sloth-ci create`` from the directory with the sloth.yml file.

That's it! Your app now listens for payload from Bitbucket at http://yourdomain:8080/docs.

Create a hook on Bitbucket, and you docs will be automatically built on every push to the repo.