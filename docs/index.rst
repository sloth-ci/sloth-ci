.. highlight:: bash

********
Sloth CI
********

.. image:: https://img.shields.io/pypi/v/sloth-ci.svg
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/dm/sloth-ci.svg
    :alt: Downloads

.. image:: https://img.shields.io/pypi/l/sloth-ci.svg
    :alt: License

.. image:: http://sloth-ci.com:8080/docs?action=shield
    :alt: Sloth CI Build Status

.. image:: https://img.shields.io/badge/chat-on_Skype-00AFF0.svg?logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABmJLR0QA%2FwD%2FAP%2BgvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH4AMVBxkJHWRrZgAAAB1pVFh0Q29tbWVudAAAAAAAQ3JlYXRlZCB3aXRoIEdJTVBkLmUHAAADL0lEQVRYw71Xu1IaURj%2BzmHxFpXdDI2Ng2OTxsnGxibF0tgGkmgLPkHkCdQnwDcAWzFKitSsMzZWrkNj48DY0DDurqMMCrsnBddlrzCSr4I9Z87%2F%2Fbfv%2FIdgFDmVxzL2Qdg3ECpa1pipgJETPCGPRVjXdgQZE4BY%2Fp2paVCWBaH8JIeBmVUAMgxyEpTQgMBv9RCUHOC9wMwqTJLBT6HoT%2BBMTSNEcpgGmClDJ0nsCZozgZzKI8IqE4c9GAkNbRLHrqCMLtFOwU3ROAAQyoNjJZyqoj0C5483tmr3QGIlDDESwucIBR%2FuZFDRDdzqJoq1FrQW846ETtaG00FwobGghrMbc4gtUM99%2BYc3ZMpNdyLMlPH9Y3wsAtmNOeyvzwaOuNZiiF%2B9QNEN5w0GS%2Fa6g%2FodJkU5R%2BPVhgm53nY0wocJcpvz7odSlu395PwIpFbDNu%2BS1w3I9Xb%2FW2yBIrc5Dyk6OE6MhLyKMoaCKmFHkCmYqXgRGM15%2FuHNYrwXjfjVi%2BV7tWF6exZiqU4KGDkZp6MSK%2BF%2B9Y8ied1AptxEptzEl9Kzb3YHQsQT1W1XbnMe6dUZWxqKtRYu6wbketvfWzckeUJQUCVwpORVhKWvH3yrXq63cVk3UKy1ghNqs7hvF8j1No7uXj338GHS14nK9hKyG3OuabJLcQAc3jVtReaF%2FfVZ36iNRaAXifjVC4S%2FT0heN3B8%2F%2BouNN02HK0d9%2Bs4oBy7hV%2BKcvi1PmPRgWHS7sXDBDo0ybh6chNfRGV7ydGjXkd4Sq8blpHupUD2ugfESMhR7ZzIjHdNs1SHgBFcjC62FhxJpFftKfBtR0LFQa%2BcP1ZAaMzpYKeLRdGNfsjFSMhR%2B4N0DhmaiBMIkYugauiH4%2FtXZMrNMcfy88cSCJXcevvg06yvwFQbJjLlJoq11gTvggADqhTlIEU5y0imtRhudROKbgQ23Hvo2N05VUVwrDT1QRUATHbkHM%2F%2FQaI7oDpL8a6gQCdrYKY8Pe9JBnuC5n9lnamJ7nsx9p6hxw%2Fh0F6EXiioUneMkiYmw0yt%2B17MO3fBOCio1nZ9hoJlpEFYyuVZ%2FwdPOB59I%2F4Dg8dx51ZL74sAAAAASUVORK5CYII%3D%0A
    :alt: Chat on Skype
    :target: https://join.skype.com/qg6XSoR9cGZ0


**Sloth CI** is a Python-based continuous integration and delivery tool that runs shell commands when you push to GitHub, Bitbucket, or GitLab. It may be building the docs, running tests, or deploying an app in a Docker container—you tell Sloth CI what to do.

Sloth CI offers detailed logs, build status badges, email notifications, and webhooks via :doc:`extensions <extensions>`. Unlike Jenkins, Sloth CI does not have a web interface. Instead, you control it via :doc:`command line <cli>` or :doc:`web API <api>`. Sloth CI is also much lighter than Jenkins in terms of memory usage.

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

#.  Create an app from it with ``sloth-ci create``, ``sci create``, or ``sci add``::

        $ sci create timestamper.yml
        App "timestamper" created
        App "timestamper" bound with config file "/path/to/timestamper.yml"

#.  Trigger the app with ``sloth-ci trigger``, ``sci trigger``, ``sci run``, or ``sci fire``::

        $ sci run timestamper
        Actions triggered on timestamper

        $ cat timestamps.txt
        Fri Feb 27 1:31:33 2016
