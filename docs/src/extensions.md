# Extensions

**Extensions** add new functionality to Sloth CI server and apps. Extensions change the way an app runs actions, add logging, send emails, add new API methods and CLI commands, and much more.

There are **app extensions** and **server extensions**.

App extensions affect only the apps which <link src="app_config.md">app config</link> they're declared in. One app can have many app extensions; moreover, it can have the same extension used many times. For example, you can use File Logs extension to write the error log and use the same extension to write the debug log to a different location.

Server extensions are invoked in the <link src="server_config.md">server config</link>. These extensions change the way Sloth CI server works. For example, Robots.txt extension protects the server from bots; this doesn't affect any particular app but affects the whole server.

Another example of a server extension is the Sloth CI API: all web API methods and CLI commands except for <link src="cli.md" title="start">cli-start</link> are implemented in an extension.

The same extension can work on both app and server levels.


## Notifications

<include repo_url="https://github.com/sloth-ci/sloth-ci-ext-notifications.git" path="README.md" sethead="2" nohead="true"></include>


## Devtools

<include repo_url="https://github.com/sloth-ci/sloth-ci-ext-devtools.git" path="README.md" sethead="2" nohead="true"></include>


## Logs

<include repo_url="https://github.com/sloth-ci/sloth-ci-ext-logs.git" path="README.md" sethead="2" nohead="true"></include>


## Docker

<include repo_url="https://github.com/sloth-ci/sloth-ci-ext-docker.git" path="README.md" sethead="2" nohead="true"></include>


## Robots.txt


## Shields.io


## SSH Exec


## Webhooks
