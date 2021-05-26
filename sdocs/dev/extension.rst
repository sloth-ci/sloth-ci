*************************
Create Your Own Extension
*************************

Sloth CI Extension is a Python module in the :ref:`apidocs-ext` subpackage. There are three areas an extension can extend:

-   :ref:`apps <dev-extension-sloth>`: apps (action execution, logging, notifications)
-   :ref:`server <dev-extension-bed>`: server (API methods, custom routes, static files)
-   :ref:`CLI <dev-extension-cli>`: command-line interface (new commands, modification of existing commands)

In the Sloth CI core, each area is implemented with a class: :class:`sloth_ci.sloth.Sloth`, :class:`sloth_ci.bed.Bed`, and :class:`sloth_ci.cli.CLI` respectively. To extend a particular area, you should extend its class.

To do that, declare a special function—:func:`extend_sloth`, :func:`extend_bed`, or :func:`extend_cli`—that returns your extended class [#why-not-just-subclass]_::

    def extend_sloth(cls, extension):
        class Sloth(cls):
            ...

        return Sloth

This isn't as hard as it may sound now. Let's create an extension together, so you can learn by example.

Tutorial
========

.. todo::

    Provide Give a step-by-step guide on extension development. 

.. _dev-extension-sloth:

.. _dev-extension-bed:

.. _dev-extension-cli:



.. rubric:: Footnotes

.. [#why-not-just-subclass] You may wonder why we declare a special function that returns a subclass instead of just declaring a subclass. The reason is that we need a way to pass the context to the extension, i.e. the params extracted from the app and server configs. We could have done it some implicit magical way, but "explicit is better that implicit."