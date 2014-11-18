***********************
Sloth CI: CI for Humans
***********************

.. image:: https://pypip.in/version/sloth-ci/badge.svg?style=flat
    :target: https://pypi.python.org/pypi/sloth-ci/
    :alt: Latest Version

.. image:: https://pypip.in/download/sloth-ci/badge.svg?style=flat
    :target: https://pypi.python.org/pypi/sloth-ci/
    :alt: Downloads

.. image:: https://pypip.in/py_versions/sloth-ci/badge.svg?style=flat
    :target: https://pypi.python.org/pypi/sloth-ci/
    :alt: Supported Python versions

.. image:: https://pypip.in/wheel/sloth-ci/badge.svg?style=flat
    :target: https://pypi.python.org/pypi/sloth-ci/
    :alt: Wheel Status

.. image:: https://pypip.in/status/sloth-ci/badge.svg?style=flat
    :target: https://pypi.python.org/pypi/sloth-ci/
    :alt: Development Status


.. toctree::
    :hidden:

    cli
    api
    components/index
    recipes/index

Sloth CI is an easy-to-use, lightweight, extendable tool that executes actions you need when certain events happen.

Sloth CI was created because Jenkins is too heavy and Buildbot was too hard to learn.

Requirements
============

Sloth CI runs with Python 3 on Windows, Linux, and Mac.

Install
=======

Install Sloth CI, the :ref:`Bitbucket <bitbucket-validator>` validator, and the :ref:`logs <logs-ext>` extension with pip:

.. code-block:: bash

    $ pip install sloth-ci sloth-ci.validators.bitbucket sloth-ci.ext.logs

Configure
=========

Create a file named *sloth.yml* in any directory and ``cd`` to that directory.

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

Create a file called something like *myapp.yml*:

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

That's it! Your app now listens for payload from Bitbucket at http://yourdomain:8080/docs.

Create a hook on Bitbucket, and the docs will be automatically built on your machine on every push to the repo.

That wasn't too hard, was it? But that's just one thing Sloth CI can do. :doc:`Learn more <components/index>` about how Sloth CI works or jump straight to :doc:`recipes <recipes/index>`.

.. note::

    Obviously, the Sloth CI server running on your machine must be accessible from the Internet for Bitbucket (or GitHub, or whatever) to be able to send you push notifications.