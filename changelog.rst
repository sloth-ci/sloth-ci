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

-   API: bind method added.
-   API: create: The config_source param renamed to config_string and can now be only a config string.
-   API: info method added to get the config file bound with an app.
-   Bed: Ability to bind an app with a config file added.
-   CLI: create: The config_source param renamed to config_file and can now be only a filepath.
-   CLI: create command now can accept multiple files.
-   CLI: If connection to the API server failed, the exception is properly handled.
-   CLI: info command added.
-   CLI: reload command added to reload an app or all apps. Useful when the bound config file has updated.
-   CLI: remove command now can accept multiple listen points.

1.0.5
=====

-   API: info: If multiple listen points were passed, an error occured. Fixed.
-   API: info: The listen_point param is now called listen_points (since there can be many of them).
-   CLI: info: Table rows are now always arranged in the same order.
-   CLI: Output messages are now saner.
-   CLI: The status command added to check the Sloth CI server status (running/not running).
-   Core: A new api package with the API server and client parts added.
-   Setup: New dependency added: tabulate.
-   Setup: New optional dependency added: sloth-ci.ext.logs.

1.0.6
=====

-   Sloth: The provider section is now optional (some apps should only be triggered manually).
-   CLI: Glob support added to the create command. You can now specify config paths like "/path/to/configs/*.yml".