********
Devtools
********

There's a special extension to help developers create extensions and validators for Sloth CI: :mod:`sloth_ci.ext.devtools`.

Before you proceed to the :doc:`extension <extension>` and :doc:`validator <validator>` tutorials, make sure you have the extension installed and enabled:

#.  Install it with pip:

    .. code-block:: bash

        $ pip install sloth_ci.ext.devtools
        ...
        Successfully installed sloth-ci.ext.devtools-1.0.1

#. Enable it in your :doc:`server config <../server-config>`:

    .. literalinclude:: _samples/sloth.yml
        :emphasize-lines: 12-14
        :language: yaml
        :caption: sloth.yml