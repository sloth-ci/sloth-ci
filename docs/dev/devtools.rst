.. highlight:: bash

********
Devtools
********

There's a special extension to help developers create extensions and validators for Sloth CI: :mod:`sloth_ci.ext.devtools`.

Before you proceed to the :doc:`extension <extension>` and :doc:`validator <validator>` tutorials, make sure you have the extension installed and enabled:

#.  Install it with pip::

        $ pip install sloth_ci.ext.devtools
        ...
        Successfully installed sloth-ci.ext.devtools-1.0.1

#.  Enable it in your :doc:`server config <../server-config>`:

    .. literalinclude:: _samples/sloth.yml
        :emphasize-lines: 12-14
        :language: yaml
        :caption: sloth.yml with devtools

Usage
=====

To create an extension or validator template, run ``sci dev`` with ``-extension`` or ``-validator`` flag::

        $ sci dev -e myextension
        Extension "myextension" created in /path/to/myextension

        $ sci dev -v my validator
        Validator "myvalidator" created in /path/to/myvalidator

By default, the template is created in the current directory. If you want to create it in a different place, use ``-destination`` flag::

        $ sci dev -e myextension -d /some/path
        Extension "myextension" created in /some/path/myextension

A template is a directory with two files: the actual extension or validator source code and a *setup.py* file:

.. literalinclude:: _samples/myextension/myextension.py
    :language: python
    :caption: Example extension source code
    
.. literalinclude:: _samples/myextension/setup.py
    :language: python
    :caption: Example extension setup file

These file will help you get started. The doctrings and function placeholders are already there for you to edit.

.. important:: Please preserve the "Description → Installation → Usage" doctring structure you see in the template source code. The doctrings are parsed to build the documentation on :doc:`extensions <../extensions>` and :doc:`validators <../validators>`.
