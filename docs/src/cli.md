# Commands

Sloth CI ships with the `sci`[^1] command line utility that lets you control the server and apps with a variety of <link title="Commands">commands</link>:

    $ sci COMMAND [OPTIONS] ...


Some commands have options, e.g. `--config`, `--level`. All options have short versions, e.g. `-c`, `-l`.

Here are the options of the `sci` command:

`-c, --config CONFIG`
:   Define path to the <link src="server_config.md">server config</link> file:

        # Start Sloth CI with a custom config:
        $ sci -c path/to/custom_config.yml start

`-h, --help`
:   Show help. Use `-h` after any command to see its help message.

`-v, --version`
:   Show the version of the locally installed Sloth CI [^2].

[^1]: When you install Sloth CI, two commands are added to your system: `sloth-ci` and `sci`. They are identical, and you can use any one you like. We use `sc` everywhere in the docs for brevity.

[^2]: `sci -v` shows the version of Sloth CI installed on your machine, i.e., the client, not the version of the server you're connecting to. To know the Sloth CI version on a remote machine, use <link title="status">`sci status`</link> command.


## Commands

### start

Start the Sloth CI server:

    $ sci start
    Starting Sloth CI on http://localhost:8080

### stop

Stop the Sloth CI server:

    $ sci stop
    Stopping Sloth CI on http://localhost:8080


### restart

Restart, i.e., <link title="stop">stop</link> then <link title="start">start</link> the Sloth CI server:

    $ sci restart
    Restarting Sloth CI on http://localhost:8080


### status

*Aliases:* `stat`, `st`

Get the status (running or not running) and version of the Sloth CI server:

    $ sci st
    Sloth CI version 2.0.1 is running on http://localhost:8080


### create

*Alias:* `add`

Create a Sloth CI app from the given config file and <link src="api.md" title="bind">bind</link> them:

    $ sci add myapp.yml
    App "myapp" created
    App "myapp" bound with config file "myapp.yml"


### history

*Aliases:* `hist`, `builds`

View paginated app build history:

    $ sci hist -l 10 -p 2 myapp
    Timestamp                 Status
    ------------------------  ------------------------------
    Mon Nov  2 21:47:10 2015  Completed 2/2
    Mon Nov  2 21:47:05 2015  Triggered, actions in queue: 2

`-l, --level LEVEL`
:   Minimal log level to show:

    40
    :   ERROR, failed builds.

    30
    :   WARNING, partially completed builds.

    20 (default)
    :   INFO, completed builds.

    10
    :   DEBUG, trigger events.

`-f, --from-page FROM_PAGE`
:   Pagination starting page. Enumeration start with 1; `-f 1` means the latest page.

`-t, --to-page TO_PAGE`
:   Pagination ending page.

`-p, --per-page PER_PAGE`
:   Number of log records per page.

`-v, --verbose`
:   Show `Level` column.


### info

Show the config file bound with the app and its latest build status:

    $ sci info myapp
    Config File    Last Build Message    Last Build Timestamp
    ------------  --------------------  -------------------------
    myapp.yml      Completed 2/2         Mon Nov  2 21:47:10 2015


### list

*Alias:* `ls`

List all available apps' listen points::

    $ sci ls
    myapp
    myotherapp


### logs

*Alias:* `lg`

View paginated app logs:

    $ sci lg -p 3 myapp
    Timestamp                 Message
    ------------------------  --------------------------------
    Mon Nov  2 21:21:58 2015  Bound with config file myapp.yml
    Mon Nov  2 21:21:58 2015  Listening on test
    Mon Nov  2 21:13:32 2015  Stopped

`-l, --level LEVEL`
:   Minimal log level to show:

    50
    :   CRITICAL, errors that don't allow apps to be created, e.g missing validator.

    40
    :   ERROR, missing extension and failed builds.

    30
    :   WARNING, partially completed builds.

    20 (default)
    :   INFO, completed builds.

    10
    :   DEBUG, stdout and stderr.

`-f, --from-page FROM_PAGE`
    Pagination starting page. Enumeration start with 1; `-f 1` means the latest page.

`-t, --to-page TO_PAGE`
    Pagination ending page.

`-p, -per-page PER_PAGE`
    Number of log records per page.

`-v, --verbose`
    Show `Level` column.


### reload

*Aliases:* `update`, `up`

Recreate the app from the bound config file. Invoke after changing the app config to apply the changes.

Reload is a shortcut for <link title="remove">remove</link> and <link title="create">create</link>:

    $ sci up myapp
    App "myapp" removed
    App "myapp" created
    App "myapp" bound with config file "myapp.yml"


### remove

*Aliases:* `del`, `rm`

Remove an app:

    $ sci rm myapp
    App "myapp" removed


### trigger

*Aliases:* `run`, `fire`

Trigger the app to run its actions. If the app doesn't use a provider, this is the only way to run its actions:

    $ sci run myapp -p foo=bar
    Actions triggered on test

`-w, --wait`
:   Block and wait for the build to finish.

`-p, --params param1=value1 param2=value2 ...`
:   List of params in the form `param=value` to be used in the actions.

    If the app's actions use params extracted from incoming payload, you must provide the necessary param replacements.
