# API

Sloth CI's API lets you restart and stop a running server, create and remove apps, list app logs and view app build history.

The API runs on the host and port specified in the <link src="server_config.md">server config</link>. It's protected from unauthorized access with basic auth; the access credentials are also stored in the server config.

The API returns data in JSON format.

There're three ways to call an API method:

-  Use Sloth CI's <link src="cli.md">CLI</link>:

        $ sci info test
        Config File        Last Build Message   Last Build Timestamp
        -----------------  -------------------  ------------------------
        /path/to/test.yml  Completed 2/2        Thu Nov  5 00:47:52 2015

-   Visit `http://mydomain.com:8080/?action=info&listen_point=test`.

-   Send POST requests with form parameters:

        $ curl -u login:password -F action=info -F listen_point=test http://mydomain.com:8080 
        {"config_file": "/path/to/test.yml", "last_build_status_message": "Completed 2/2", "last_build_status_level": "INFO", "last_build_timestamp": 1621191160.9056282} 


## Methods

### create

Create an app from the given config string:

    $ curl -u login:password -F action=create -F config_string=$(cat test.yml) http://mydomain:8080
    "test"

`config_string`
:   URL-encoded <link src="app_config.md">app config</link>.


### bind

If the app is <link title="create">created</link> from a config file, bind them together, so Sloth CI would know where to read the config from when you <link src="cli.md" title="reload">reload</link> the app:

    $ curl -u login:password  -F action=bind -F listen_point=test -F config_file=/path/to/test.yml http://mydomain:8080
    null

`listen_point`
:   App listen point.

`config_file`
:   Path to the config file ti bind with the app.

The <link src="cli.md" title="create">create</link> CLI command runs the <link title="create">create</link> and <link title="bind">bind</link> API methods.


### trigger

Trigger app's actions:

    $ curl -u login:password -F action=trigger -F listen_point=test -F foo=bar http://mydomain:8080
    null

Trigger app's actions and wait for them to complete:

    $ curl -u login:password -F action=trigger -F listen_point=test -F wait=1 -F success_url=http://example.com/success -F fail_url=http://example.com/fail -F foo=bar http://mydomain:8080
    "Completed 2/2"

`listen_point`
:   App listen point.

`wait` *optional*
:   Wait for the actions to complete.

`success_url` *optional*
:   URL to redirect to after a successful build run. Used only with `wait`.

`fail_url` *optional*
:   URL to redirect to after a failed or incomplete build run. Used only with `wait`.

custom params *optional*
:   Any number of params to replace <link src="app_config.md" title="Params">placeholders</link> in the actions.


### info

Get app config file path and last build status:

    $ curl -u login:password -F action=info -F listen_point=test -s http://mydomain:8080 | jq
    {
        "config_file": "C:\\Users\\moigagoo\\Projects\\sloth-ci\\test.yml",
        "last_build_status_level": "INFO",
        "last_build_status_message": "Completed 2/2",
        "last_build_timestamp": 1448695186.978541
    }


### history

Get app build history:

    $ curl -u login:password -F action=history -F listen_point=test -s http://mydomain:8080 | jq
    [
        {
            "level_name": "INFO",
            "level_number": 20,
            "logger_name": "test.build",
            "message": "Completed 2/2",
            "timestamp": 1448695186.978541
        },
        ...

Paginate and filter by status:

    $ curl -u login:password -F action=history -F listen_point=test -F from_page=3 -F per_page=2 -F level=10 -s http://mydomain:8080 | jq
    [
        {
            "level_name": "INFO",
            "level_number": 20,
            "logger_name": "test.exec",
            "message": "Executing action: PowerShell echo Good morning!",
            "timestamp": 1448695185.3463366
        },
        ...

`listen_point`
:   App listen point.

`from_page`, `to_page`, `per_page`
:   Pagination params.

    By default, `from_page` = 1, `to_page` = `from_page`, `per_page` = 10.

`level`
:   Minimal log level to show:

    40
    :   ERROR, failed builds.

    30
    :   WARNING, partially completed builds.

    20 (default)
    :   INFO, completed builds.

    10
    :   DEBUG, trigger events.


### logs

Get app logs:
 
    $ curl -u login:password -F action=logs -F listen_point=test -s http://mydomain:8080 | jq
    [
        {
            "level_name": "INFO",
            "level_number": 20,
            "logger_name": "test.build",
            "message": "Completed 2/2",
            "timestamp": 1448695186.978541
        },
        ...

Paginate and filter by log level:

    $ curl -u login:password -F action=logs -F listen_point=test -F from_page=3 per_page=2 level=10 -s http://mydomain:8080 | jq
    [
        {
            "level_name": "INFO",
            "level_number": 20,
            "logger_name": "test.exec",
            "message": "Executing action: PowerShell echo Good morning!",
            "timestamp": 1448695185.3463366
        },
        ...

`listen_point`
:   App listen point.

`from_page`, `to_page`, `per_page`
:   Pagination params.

    By default, `from_page` = 1, `to_page` = `from_page`, `per_page` = 10.

`level`
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


### list

List existing app listen points:

    $ curl -u login:password -F action=list -s http://mydomain:8080 | jq
    [
        "test"
    ]


### remove

Remove the app:

    $ curl -u login:password -F action=remove -F listen_point=test http://mydomain:8080


### version

Get the version of the Sloth CI server:

    $ curl -u login:password -F action=version http://mydomain:8080
    "2.0.1"


### restart

Restart the Sloth CI server:

    $ curl -u login:password -F action=restart http://mydomain:8080
    null


### stop

Stop the Sloth CI server:

    $ curl -u login:password -F action=stop http://mydomain:8080
    null

