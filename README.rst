***********************
Sloth CI: CI for Humans
***********************

.. image:: https://img.shields.io/pypi/v/sloth-ci.svg?style=flat-squar
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/dm/sloth-ci.svg?style=flat-square
    :alt: Downloads

.. image:: https://img.shields.io/pypi/l/sloth-ci.svg?style=flat-square
    :alt: License

.. image:: sloth-weed-small.jpg
    :align: center
    :alt: Logo

Sloth CI is an easy-to-use, lightweight, extendable tool that executes actions you need when certain events happen.

Sloth CI was created because Jenkins is too heavy and Buildbot was too hard to learn.

Read the docs at http://sloth-ci.com/ (btw, Sloth CI builds them).

Requirements
============

Sloth CI runs with Python 3.3+ on Windows, Linux, and Mac.

Install
=======

Install Sloth from `PyPI <https://pypi.python.org/pypi/sloth-ci>`__ with pip:

.. code-block:: bash

    $ pip install sloth-ci

It's also a good idea to install a validator for Bitbucket or GitHub right away:

.. code-block:: bash

    $ pip install sloth-ci.validators.bitbucket
    $ pip install sloth-ci.validators.github

Configure
=========

Create a file named *sloth.yml* in any directory and cd to that directory.

Here's how your *sloth.yml* can look like:

.. code-block:: yaml

    host: localhost
    port: 8080

    daemon: true

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

Create a file called *myapp.yml*:

.. code-block:: yaml

    listen_point: docs

    work_dir: ~/projects

    provider:
        bitbucket:
            owner: username
            repo: repository
            branches:
                - master
                - staging

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

Contribute
==========

`Report a bug <https://bitbucket.org/moigagoo/sloth-ci/issues/new>`__

`Fork and improve <https://bitbucket.org/moigagoo/sloth-ci/fork>`__
