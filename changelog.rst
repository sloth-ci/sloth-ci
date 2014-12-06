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

-   Sloth: The "provider" section is now optional (some apps should only be triggered manualy).
-   CLI: Glob support added to the "create" command. You can now specify glob paths like "/path/to/configs/*.yml".
-   Server config: New section "config_paths" added. Apps will be created from the given config files. You can now specify glob paths like "/path/to/configs/*.yml".

1.0.7
=====

-   CLI: reload: ConnectionError is now properly handled.
-   CLI: reload: If an app's listen point was changed in the bound config file, the newly created app failed to bind to it after being created. Fixed.

1.0.8
=====

-   API: The "logs" method added to get app logs.
-   Bed: Database logging added by default.
-   Bed: Unbound apps could not be removed on server stop. Fixed.
-   Server config: New section "paths" added with params "access_log", "error_log", and "db" point to the access log, error log, and database files respectively.
-   Server config: The "config_paths" section moved to the "paths: configs" subsection.
-   Server config: The "log_dir" param replaced with the "paths: access_log" and "paths: error_log" params.

1.0.9
=====

-   API: Client: The "history" API method support added.
-   API: Client: The "logs" API method support added.
-   API: Server: info: The "last_build_status" field added to the output.
-   API: Server: The "history" method added to get paginated app build history.
-   CLI: info: The "Last Build Status" column added.
-   CLI: The "history" action added.
-   CLI: The "logs" action added.
-   DB logging moved to a separate built-in extension.
-   DB build history tracking added as a separate built-in extension.
-   Sloth: Extensions: The "extend" function now accepts the extension name + its config instead of just name.