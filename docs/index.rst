.. highlight:: bash

********
Sloth CI
********

.. image:: https://img.shields.io/pypi/v/sloth-ci.svg?style=flat-square
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/dm/sloth-ci.svg?style=flat-square
    :alt: Downloads

.. image:: https://img.shields.io/pypi/l/sloth-ci.svg?style=flat-square
    :alt: License


**Sloth CI** is a Python-based tool that builds docs, runs tests, and deploys your code when you push to GitHub, Bitbucket, or GitLab. Just type the commands you'd normally run manually and let Sloth CI run them for you!

Quickstart
==========

#.  Install Sloth CI with pip::

        $ pip install sloth-ci

    **Sloth CI** requires Python 3.4+ and works on Linux, Windows, and Mac OS X.

    Optionally, to make logs colorful, install `colorama <https://pypi.python.org/pypi/colorama>`_::

        $ pip install colorama

#.  Create a file called :download:`sloth.yml <_samples/sloth.yml>` with this content:

    .. literalinclude:: _samples/sloth.yml
        :language: yaml

#.  Run ``sloth-ci start`` or ``sci start``::

        $ sci start &
        Starting Sloth CI on http://localhost:8080

    Go to http://localhost:8080?action=version in your browser and enter the login and password from the server config (``myname`` and ``mypass`` in the example above). You should see the Sloth CI version:

    .. image:: _images/check-version.png

#.  Create a file called :download:`timestamper.yml <_samples/timestamper.yml>`:

    .. literalinclude:: _samples/timestamper.yml
        :language: yaml

#.  Create the app from it with ``sloth-ci create``, ``sci create``, or ``sci add``::

        $ sci create timestamper.yml
        App "timestamper" created
        App "timestamper" bound with config file "/path/to/timestamper.yml"

#.  Trigger the app with ``sloth-ci trigger``, ``sci trigger``, ``sci run``, or ``sci fire``::

        $ sci run timestamper
        Actions triggered on timestamper

        $ cat timestamps.txt
        Fri Feb 27 1:31:33 2016
