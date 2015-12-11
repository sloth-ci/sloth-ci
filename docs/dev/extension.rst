*************************
Create Your Own Extension
*************************

Basics
======

Sloth CI extensions are Python modules in the :ref:`apidocs-ext` subpackage.

Here's an extension that prints "Live slow, die whenever" after every action execution::

    def extend_sloth(cls, extension):
        class Sloth(cls):
            def execute(self, action):
                print('Live slow, die whenever')
                super().execute(action)

        return Sloth

Put this into */path/to/site-packages/sloth_ci/ext/myextension.py* and declare the extension in the :doc:`app config <../app-config>`:

.. code-block:: yaml

    extensions:
        myextension:
            module: myextension

Trigger actions on the app and see the motto printed:

.. code-block:: bash

    $ sci run test -w
    Live slow, die whenever
    Live slow, die whenever
    Completed 2/2


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