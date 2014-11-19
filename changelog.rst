1.0.0
=====

-   First major version. Changelog started.

1.0.1
=====

-   The ``-d`` (``--daemon``) CLI flag removed (it was not working anyway).

1.0.2
=====

-   CLI: trigger: if no params were passed, an error would occur. Fixed.
-   Bed: add_sloth: TypeError is now handled, interpeted as config source is not a file path or a valid config string.
-   API: create: TypeError is now handled, interpeted as config source is not a file path or a valid config string. Using absolute path is advised.
-   CLI: Message on Sloth CI start added.

1.0.3
=====

-   Sloth: Validation: The provider dict was emptied on first payload check, so all the following ones did not work. Fixed.

1.0.4
=====

-   CLI: If connection to the API server failed, the exception is properly handled.
-   API: create: The config_source param renamed to config_string and can now be only a config string.
-   CLI: create: The config_source param renamed to config_file and can now be only a filepath.