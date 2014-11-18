***********************
Sloth CI: CI for Humans
***********************

.. image:: https://pypip.in/version/sloth-ci/badge.svg?style=flat
    :target: https://pypi.python.org/pypi/sloth-ci/
    :alt: Latest Version

.. image:: https://pypip.in/download/sloth-ci/badge.svg?style=flat
    :target: https://pypi.python.org/pypi/sloth-ci/
    :alt: Downloads

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

Install Sloth CI with pip:

.. code-block:: bash

    $ pip install sloth-ci

Configure
=========

Create a file named *sloth.yml* in any directory and ``cd`` to that directory.

Here's how your sloth.yml can look like:

.. code-block:: yaml

    host: localhost

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

    listen_point: myapp/incoming

    work_dir: ~/projects

    provider:
        bitbucket:
            repo: spam/eggs

    extensions:
        error_logs:
            module: logs
            path: /var/log/sloth-ci/myapp
            filename: myapp_errors.log
            level: ERROR

    actions:
        - hg pull {branch} -u {repo_dir}
        - sphinx-build -aE {repo_dir}/docs {output_dir}

    params:
        repo_dir: eggs
        output_dir: /var/www/myapp_docs 

Create the app from the config:

.. code-block:: bash

    $ sloth-ci create myapp.yml
    App created, listening on myapp/incoming

That's it! Your app now listens for payload from Bitbucket at http://localhost:8080/myapp/incoming.

Create a hook on Bitbucket, and the docs will be automatically built on your machine on every push to the repo.

That wasn't too hard, was it? But that's just one thing Sloth CI can do. :doc:`Learn more <components/index>` about how Sloth CI works or jump straight to :doc:`recipes <recipes/index>`.

.. note::

    Obviously, the Sloth CI server running on your machine must be accessible from the Internet for Bitbucket (or GitHub, or whatever) to be able to send you push notifications.