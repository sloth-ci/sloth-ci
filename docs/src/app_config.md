# App Config

**App config** contains the settings for a Sloth CI app:

-   unique <link title="Listen Point">listen point</link>
-   <link title="Provider">provider</link> that triggers actions
-   <link title="Actions">actions</link> to run, <link title="Params">params</link> to run them with, and the <link title="Work Dir">directory</link> to run them in
-   <link title="Extensions">extensions</link>

Sample app config:

    id: myapp # or "name: myapp", or "listen_point: myapp"

    provider:
        github:
            owner: username
            repo: repo
            branches:
                - dev
                - staging

    actions:
        - !critical touch {filename}
        - echo "The branch is {branch}" >> {filename}

    params:
        filename: myfile.txt

    work_dir: ~/apps/myapp

    exec_timeout: 5

    extensions:
        debug_logs:
            module: file_logs
            path: /var/log/myapp/
            filename: myapp_debug.log
            level: DEBUG

The config is in YAML format. When you create an app with the <link src="cli.md" title="create">create</link> command, provide the config as a path to a .yml file:

    $ sci create /path/to/test.yml

When you create an app <link src="api.md" title="create">via the API</link>, provide the config as a URL-encoded string:

    $ http -f -a login:password localhost:8080 \
            action=create \
            config_string=$(cat test.yml)
    HTTP/1.1 201 Created
    Content-Length: 6
    Content-Type: application/json
    Date: Fri, 27 Nov 2015 21:39:58 GMT
    Server: CherryPy/3.8.0

    "test"


## Listen Point

*required*

Every app has a unique URI called *listen point*. If the server is running on *example.com:8080*, and the app's listen point is *test*, the full path to the app is *http://example.com:8080/test*.

Listen point can contain slashes. Listen point *must not* start or end with a slash.


## Provider

Although you can <link src="cli.md" title="trigger">trigger</link> app's actions manually, Sloth CI's true strength is to run actions automatically, e.g., when you push to GitHub.

A service that sends the trigger events is called a *provider*. To work with a certain provider, Sloth CI must have a matching <link src="validators.md">validator</link> installed. The `provider` param in an app config actually points to the matching *validator*.

<link src="validators.md">See available validators and their params →</link>

!!! tip
    If you want to trigger the app manually only, skip the whole `provider` section.


## Actions

List of actions to run. Each action is a shell command. Commands are executed one by one top to bottom.

Actions can contain placeholders enclosed between curly brackets: `{filename}`, `{branch}`. The placeholders are overridden with values in this order:

1. params from the <link title="Params">params</link> section
1. params extracted by the <link src="validators.md">validator</link>
1. params provided with the <link src="cli.md" title="trigger">trigger</link> command or via the <link src="api.md" title="trigger">trigger</link> API method

Actions can contain stream redirects with `>` and `>>`. Actions *must not* contain context changes like `cd` or `source`.

If you want the whole build to fail when a particular action fails, mark the action with `!critical` tag.


## Params

Values for the placeholders in <link title="Actions">actions</link>.


## Work Dir

The directory to run the actions in. By default, the actions are executed in the directory you launched Sloth CI in, i.e., `work_dir="."`.

!!! tip
    The `work_dir` param is optional, but it's highly recommended you to specify it. You want to be 100% sure your `rm -rf *` runs in the right place.


## Exec Timeout

The maximal allowed time in seconds for an action to run. If an action takes longer than `exec_timeout` seconds to execute, it's terminated.

By default, there's no timeout.


## Extensions

App-level <link src="extensions.md">extension</link> declarations.

A declaration has a unique name (e.g., `debug_logs`) and must contain the extension module name (e.g., `file_logs`). Depending on the extension, a declaration can include additional params. For example, File Logs extension has eight params.

You can declare the same extension module multiple times under different names:

    extensions:
        debug_logs:
            module: file_logs
            path: /var/log/myapp/
            filename: myapp_debug.log
            level: DEBUG
        info_logs:
            module: file_logs
            path: /var/log/myapp/
            filename: myapp_info.log
            level: INFO

No extensions are declared by default.
