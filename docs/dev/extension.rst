*************************
Create Your Own Extension
*************************

Sloth CI Extension is a Python module within the :ref:`apidocs-ext` subpackage. There are three areas an extension can extend:

-   :ref:`apps <dev-extension-sloth>`: execution, logging, notifications
-   :ref:`server <dev-extension-bed>`: API methods, custom routes, static files
-   :ref:`CLI <dev-extension-cli>`: new commands, modification of existing commands

In the Sloth CI core, each area is implemented by a class: :class:`sloth_ci.sloth.Sloth`, :class:`sloth_ci.bed.Bed`, and :class:`sloth_ci.cli.CLI` respectively. To extend an area, you extend the matching class.

To extend a class, declare a special function—:func:`extend_sloth`, :func:`extend_bed`, or :func:`extend_cli`—and declare your extended class inside it [#why-not-just-subclass]_::

    def extend_sloth(cls, extension):
        class Sloth(cls):
            ...

        return Sloth

It all may seem complicated for now, but don't worry, it's much simpler in reality than it sounds.

Let's create a simple extension.


.. _dev-extension-devtools:

Devtools
========

There's a special extension to help developers create extensions and validators: :mod:`sloth_ci.ext.devtools` for Sloth CI.

#.  Install it with pip:

    .. code-block:: bash

        $ pip install sloth_ci.ext.devtools
        ...
        Successfully installed sloth-ci.ext.devtools-1.0.1

#. Enable it in the :doc:`server config <../server-config>`:

    .. literalinclude:: _samples/sloth.yml
        :emphasize-lines: 12-14
        :language: yaml
        :caption: sloth.yml


#. Run ``sci dev -e spam`` to create an extension called "spam":

    .. code-block:: bash
        
        $ sci dev -e spam
        Extension "spam" created.
                   
    This command creates a directory "spam" with the extension template and a *setup.py* file:

    .. code-block:: bash

        $ ls spam
        setup.py spam.py

    The template contains three dummy functions:

    .. literalinclude:: _samples/spam.py
        :caption: spam.py


.. _dev-extension-sloth:

Extending Apps
==============


.. _dev-extension-bed:

Extending Server
================


.. _dev-extension-cli:

Extending CLI
=============

Distributing Extensions
=======================

.. rubric:: Footnotes

.. [#why-not-just-subclass] You may wonder why we declare a special function that returns a subclass instead of just declaring a subclass. The reason is that we need a way to pass the context to the extension, i.e. the params extracted from the app and server configs. We could have done it some implicit magical way, but "explicit is better that implicit."