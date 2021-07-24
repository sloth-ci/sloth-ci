# Server Config

**Server config** contains the settings for the Sloth CI server:

-   <link title="Host, Port">host and port</link> to run on
-   <link title="API Access Credentials">login and password to access the <link src="api.md">API</link>
-   <link title="Paths">paths to the db, logs, and default <link src="app_condig.md">app configs</link>
-   <link title="Extensions">extensions</link>
-   <link title="Daemon">daemon status</link>

Sample server config:

    host: 0.0.0.0
    port: 8080

    auth: # or api_auth
        -   login: alice
            password: password
        -   login: bob
            password: secret

    paths:
        access_log: /usr/log/sloth-ci/access.log
        error_log: /usr/log/sloth-ci/error.log

        db: /etc/sloth-ci/sloth.db

        configs:
            - /etc/conf.d/sloth-ci/*.yml

    extensions:
        hide-from-robots:
            module: robots_txt

    daemon: true

By default, Sloth CI tries to use a file called *sloth.yml* in the current directory as a server config, but you can specify a custom one with the <link src="cli.md">`--config, -c`</link> param:

    $ sci -c /path/to/myconfig.yml start


## Host, Port

*required*

The host and port for the Sloth CI server to run on.

To make the server accessible from the Internet, set `host` to `0.0.0.0`.


## API Access Credentials

List of logins and passwords to access the <link src="api.md">Sloth CI API</link>. Skipping this section lets anyone use your API without authentication (so be careful with it!).

If there's only one pair, you may omit putting it in a list:

    auth:
        login: john
        password: secret


## Paths

!!! tip
    Use absolute paths. Relative paths work too, but absolute ones are more reliable.

access_log
:   Path to the log that records all incoming requests.

    Default value: `sloth_access.log`

error_log
:   Path to the log that records app creation and extension loading errors, server startup and tier down info.

    Default value: `sloth_error.log`

db
:   Path to the SQLite DB file to store the app logs in.

    Default value: `sloth.db`

configs
:   List of paths to the <link src="app_config.md">app configs</link> to load on server startup.

    Items can be file paths or glob patterns:

        configs:
            - /path/to/app.yaml
            - /path/to/configs/*.yml

    No app configs are loaded by default.


## Extensions

Server-level <link src="extensions.md">extension</link> declarations.

A declaration has a unique name (`hide-from-robots`) and must contain the extension module name (`robots_txt`). Depending on the extension, a declaration can include additional params. For example, the mentioned <link src="extensions.md" title="Robots.txt">Robots.txt</link> extension has two optional params: `file` and `path`.

You can declare the same extension module multiple times under different names:

    extensions:
        hide-from-robots:
            module: robots_txt
        robots-txt-on-a-different-path:
            module: robots_txt
            path: /static/robots.txt

No extensions are declared by default.


## Daemon

Run Sloth CI as a daemon. Default is `false`.

!!! important
    This params works only in UNIX-based systems. If you launch Sloth CI with `daemon: true` on Windows, it will crash.
