# 2.1.1

-   Bed, API: Bed: Code refactored to allow extending app listener.


# 2.1.0

-   Server config: Auth section can now contain multiple login:password pairs.


# 2.0.9

-   CLI: Fixed a critical issue with not working CLI if API auth was provided.


# 2.0.8

-   API: Trigger: When invoking `trigger` directly via web API with `wait=1`, you can now define the `success_url` and `fail_url` params to be redirected to after the build completes or fails.
-   API: Auth is now optional.


# 2.0.7

-   App config: Actions can be marked critical with the `!critical` tag.


# 2.0.6
-   Fixed an issue with incorrectly handled `auth` alias.


# 2.0.5

-   CLI: Failed actions now return non-zero exit code.
-   App config: Aliases for `listen_point` added: `id` and `name`.


# 2.0.4

-   Server config: An alias for `api_auth` added—`auth`.

# 2.0.3

-   Colorama is now an optional dependency.


# 2.0.2

-   Extension would not load if any extension function was missing. Fixed.


# 2.0.1

-   API: trigger: `wait` param added: block until the triggerred actions are completed.
-   Bed: Payload json is now parsed before the request is passed to a validator.
-   CLI: Help texts improved.
-   CLI: trigger: `-wait` flag added: block until the triggerred actions are completed.
-   Setup: Built-in extensions were not properly installed. Fixed.


# 2.0.0

-   API CLI vocabulary changed.
-   API reimplemented as a built-in extension.
-   A single extension can now extend apps, server, and CLI with `extend_sloth`, `extend_bed`, and `extend_cli` functions.
-   CLI: Cliar is now used instead of docopt.
-   Tons of small changes.


# 1.3.0

-   Bed: Server extensions now can override all Bed methods.


# 1.2.9

-   API: Server: Bind: Config file binding didn't work. Fixed.
-   CLI: Info: Info didn't work. Fixed.


# 1.2.8

-   Code cleanup.
-   Bed: Server extension support added.


# 1.2.7

-   CLI: history output is now colorized.
-   CLI: Level column hidden from history and info output.


# 1.2.6

-   API: Server: info now returns build status levels too.
-   CLI: Colorization is now possible based on any column.
-   CLI: info output is now colorized.


# 1.2.5

-   API: info: If the database is unavailable, only build statuses are not returned.
-   API: info: The info method didn't work if the database was unavailable. Fixed.
-   API: Web: Alias for info added: list.
-   API: Web: history, logs: If the database is unavailable, the history and logs methods are still accessible but explicitly return errors.
-   Server config: DB path can only point to a file. Previous decision to allow directories led to ambiguity.
-   Server config: If the DB path was null (or false, or 0), no apps could be created. Fixed.


# 1.2.4

-   Build: Exec: Support for stream redirection and shell commands added.
-   Server config: DB path can now point to a directory; sloth.db will be created automatically.
-   Build logging: Trigger events are now logged with level DEBUG, not INFO.
-   Util: SqliteHandler: Exception handling on event emitting added.


# 1.2.3

-   Apps with listen points  "_"  and "x/y" were not logged. Fixed.
-   Listen points are used to refer to apps instead of names (i.e. slugs).
-   Removed dependency awesome-slugify.
-   Sloth: The "name" attribute replaced with "listen_point".


# 1.2.2

-   CLI: info: Alias added: list.


# 1.2.1

-   CLI, API: Logs: If a listen point did not exist, an empty list was returned instead of an error. Fixed.
-   Build: Exec: All failed executions were logged with the same "__init__ missing cmd" error. Fixed.
-   Build: Exec: Failed actions are logged as error, not critical.
-   Build: Exec: If an action failed, its stdout and stderr were not logged. Fixed.
-   Build: Exec: In an action fails, its exit code is logged as error. The stdout and stderr are logged as debug, as usual.


# 1.2.0

-   Build: Logging: Params are now stored by the exec logger, not the build logger. This keeps build history clean.


# 1.1.9

-   Build: Action execution: If stderr is not empty, the action is considered failed.
-   CLI: Logs: Tables are now colorized.
-   Logging: Minor improvements in build logging.
-   New dependency: colorama.
-   Payload handling: Single payload can now trigger multiple builds. Useful for combined pushes with commits from multiple branches.


# 1.1.8

-   API: Server: info: Info was broken if at least one app was never triggered. The default timestamp is now 0. Fixed.


# 1.1.7

-   API: Server: bind: Local variable e was called before assignment. Fixed.
-   Bed: Create app: Listen point conflict: Wrong variable was referenced in the error message. Fixed.


# 1.1.6

-   API: Server: logs: Log level filtering didn't work. Fixed.
-   API: Server: info: The records are now sorted by the last build timestamp.


# 1.1.5

-   Ext: Build history: The "Failed" status indicates the failed action and the exception raised.
-   Ext: Build history: The "Triggered" status indicates params.
-   Logging: The build logger added to Sloth.
-   Logging: The "processing" logger renamed to "exec."
-   Sloth: Exec params persisted between builds, resulting in false successes. Fixed.
-   Sloth: Build trigger is now logged with level DEBUG.


# 1.1.4

-   CLI: The "version" command removed.
-   CLI: Remote server version is now shown in the "status" command output.


# 1.1.3

-   API: Client: The "version" API method support added.
-   API: Server: The "version" method added to get the server version.
-   CLI: The "version" command added.


# 1.1.2

-   Ext: Build history: The "Triggered" status is added before action queue execution.


# 1.1.1

-   Ext: Build history: Build status was set to 'Never triggered' on every app creation. Fixed.


# 1.1.0

-   API: Server: info: The "last_build_timestamp" field added to the output.
-   CLI: info: The "Last Build Timestamp" column added.


# 1.0.9

-   API: Client: The "history" API method support added.
-   API: Client: The "logs" API method support added.
-   API: Server: info: The "last_build_status" field added to the output.
-   API: Server: The "history" method added to get paginated app build history.
-   CLI: info: The "Last Build Status" column added.
-   CLI: The "history" command added.
-   CLI: The "logs" command added.
-   DB logging moved to a separate built-in extension.
-   DB build history tracking added as a separate built-in extension.
-   Sloth: Extensions: The "extend" function now accepts the extension name + its config instead of just name.


# 1.0.8

-   API: The "logs" method added to get app logs.
-   Bed: Database logging added by default.
-   Bed: Unbound apps could not be removed on server stop. Fixed.
-   Server config: New section "paths" added with params "access_log", "error_log", and "db" point to the access log, error log, and database files respectively.
-   Server config: The "config_paths" section moved to the "paths: configs" subsection.
-   Server config: The "log_dir" param replaced with the "paths: access_log" and "paths: error_log" params.


# 1.0.7

-   CLI: reload: ConnectionError is now properly handled.
-   CLI: reload: If an app's listen point was changed in the bound config file, the newly created app failed to bind to it after being created. Fixed.


# 1.0.6

-   Sloth: The "provider" section is now optional (some apps should only be triggered manualy).
-   CLI: Glob support added to the "create" command. You can now specify glob paths like "/path/to/configs/*.yml."
-   Server config: New section "config_paths" added. Apps will be created from the given config files. You can now specify glob paths like "/path/to/configs/*.yml."


# 1.0.5

-   API: info: If multiple listen points were passed, an error occured. Fixed.
-   API: info: The listen_point param is now called listen_points (since there can be many of them).
-   CLI: info: Table rows are now always arranged in the same order.
-   CLI: Output messages are now saner.
-   CLI: The status command added to check the Sloth CI server status (running/not running).
-   Core: A new api package with the API server and client parts added.
-   Setup: New dependency added: tabulate.
-   Setup: New optional dependency added: sloth-ci.ext.logs.


# 1.0.4

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


# 1.0.3

-   Sloth: Validation: The provider dict was emptied on first payload check, so all the following ones did not work. Fixed.


# 1.0.2

-   CLI: trigger: if no params were passed, an error would occur. Fixed.
-   Bed: add_sloth: TypeError is now handled, interpeted as config source is not a file path or a valid config string.
-   API: create: TypeError is now handled, interpeted as config source is not a file path or a valid config string. Using absolute path is advised.
-   CLI: Message on Sloth CI start added.


# 1.0.1

-   The "-d" ("--daemon") CLI flag removed (it was not working anyway).


# 1.0.0

-   First major version. Changelog started.

