# CLI

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

[^2]: `sci -v` shows the version of Sloth CI installed on your machine, i.e. the client, not the version of the server you're connecting to. To know the Sloth CI version on a remote machine, use <link title="status">`sci status`</link> command.


## Commands

### status

### create

### reload

