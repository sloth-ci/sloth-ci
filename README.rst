*****
sloth
*****

.. image:: https://pypip.in/v/sloth-ci/badge.png
    :target: https://crate.io/packages/sloth-ci/
    :alt: Latest PyPI version

.. image:: https://pypip.in/d/sloth-ci/badge.png
    :target: https://crate.io/packages/sloth-ci/
    :alt: Number of PyPI downloads

CI can be a bitch.

Jenkins is nice, but it's Java, thus the memory consumption.

Buildbot is really hairy and weird.

**Sloth** is simple. Try it!

.. image:: https://dl.dropbox.com/u/43859367/napoleon_sloth.jpg
    :align: center
    :width: 200

Installation
============

Run ``install.sh`` as root (the root priveleges are required to copy the default configs to ``/etc/sloth/`` and to copy the ``run-sloth`` executable to ``/usr/bin/``.)

Usage
=====

run-sloth [-h] [--host HOST] [--port PORT] config [config ...]

positional arguments:
  config

optional arguments:
  -h, --help   show this help message and exit
  --host HOST
  --port PORT

The Sloth server config can be found and edited in ``/etc/sloth/server.conf``. Also, ``host`` and ``port`` parameters can be defined directly as eponymous optional command line arguments.

Each Sloth instance is fully defined by its **config**. A config is a simple INI-formatted file with the following fields (example from ``/etc/sloth/default.conf``:)

::

    ;URL path to listen to.
    ;listen_to = /sloth

    ;Work directory to perform the actions in.
    ;work_dir = ~/sloth/

    ;Request provider. See the list of available providers in the docs.
    ;provider = bitbucket

    ;Data required to validate payload from a provider. See the required data for each provider in the docs.
    [provider_data]
    ;repo = moigagoo/sloth
    ;branch = default

    ;Actions to perform (command line commands, command per line.)
    [actions]
    ;echo Hi, sloth

    ;Nodes to broadcast the message to.
    [nodes]
    ;htts://example.com/sloth

.. note:: Pay attention that unsectioned params *must* be declared first.

It may be a good idea to put your app Sloth config in the app repo.

``listen_to``
-------------

Each Sloth instance listens on its own path on the server and port defined in the server config (see above.)

For example, if the ``listen_to`` param is "my_app" and the default ``server.conf`` is used, the Sloth instance will listen to ``http://127.0.0.1:8080/my_app/``.

``work_dir`` and ``actions``
----------------------------
The ``actions`` section contains the list of actions to be performed when a request comes to the SLoth instance.

The directory, in which Sloth must operate is declared in ``work_dir``. This is your application directory.

For example, if you have an Mercurial-driven app in ``/home/user/app/my_app/`` and you want to get the latest updates on each push to the repo, you should set the ``work_dir`` param to ``/home/user/app/my_app/``, and your ``actions`` section may look something like this:

::

    [actions]
    hg pull
    hg up

``provider`` and ``provider_data``
----------------------------------

The ``provider`` param declares what kind of request the Sloth instance must expect or, in other words, what the origin and nature of the expected requests are.

A provider can use additional data to validated the incoming payload; these data are declared in the ``provider_data`` section.

Currently (v. 0.1.7,) two providers are supported: **dummy** and **bitbucket**.

The ``dummy`` provider serves for testing purposes. Its only ``provider_data`` param is ``message``, and the payload is considered valid if it equals the message.

The ``bitbucket`` provider expects Bitbucket POST-requests sent on every push (should be enabled in the repo settings.) It validates the payload against the repo name and branch—the ``repo`` and ``branch`` params of the ``provider_data`` section respectively.

``nodes``
---------

Sloth not only can perform actions on receiving requests, but also can distibute it further to other Sloth nodes.

These nodes are listed in the ``nodes`` section.
