************
Applications
************

Sloth CI application is an independant worker with its own config. Every app has a unique listen point, by which it can be referred to. When payload comes on particular listen point, the :doc:`server <server>` will direct it to the respective app.

The app will validate the payload, extract useful data from it, and attempt to execute the specified actions.

An app spawns a thread every time it needs to execute actions.

.. _app-config:

App Config
==========

.. literalinclude:: ../sample.yml
    :language: yaml