*************************
Migrating from Sloth CI 1
*************************

.. todo::

    The configs are backward compatible except for the ``provider`` section.
    
    Starting with version 2, extensions should implement ``extend_sloth``, ``extend_bed``, or ``extend_cli`` functions, not ``extend`` like before. The old ``extend`` function corresponds to the new ``extend_sloth`` one.