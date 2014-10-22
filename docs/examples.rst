****************************
Examples: Sloth CI in Action
****************************

Build Sphinx Docs
=================

Suppose you have your docs in a GitHub repo *username/repo*.

On every commit you want to get the latest version and build the docs into a directory, e. g. */var/www/docs* (given you're on Linux).

Extensions
----------

    -   logs

App Config
----------

::

    provider = github

    [provider_data]
    repo = username/repo

    [extensions]
    logs

    [params]
    repo_dir = ~/repos/docs
    output_dir = /var/www/docs

    [actions]
    git -C {repo_dir} pull --rebase origin {branch}
    sphinx-build -aE {repo_dir} {output_dir}

Save this content in a file called *docs.conf* in the */etc/sloth-ci/configs/apps* directory.

Given Sloth CI is already running, it will listen for GitHub payload on *YOURDOMAIN/docs*.

Connect GitHub
--------------

Go to the repo page on GitHub and add a new commit hook pointing to *YOURDOMAIN/docs*.

Update Repo on Many Servers via SSH
===================================

Suppose you have a bunch of servers (e.g. foo.com, bar.com, and 123.45.67.89), all hosting the same Mercurial repo stored on Bitbucket (e.g. username/repo). When the repo is updated, you want to update the repo on all servers.

The access the first two, we have SSH keys in the system's default location, and the third one is accessed with a password "knock".

Extensions
----------

    -   logs
    -   ssh-exec

App Config
----------

::

    work_dir = ~/repos/repo

    stop_on_first_fail = True

    provider = bitbucket

    [provider_data]
    repo = username/repo

    [extensions]
    logs
    ssh-exec
    
    [ssh-exec]
    hosts = foo.com, bar.com, 123.45.67.89
    username = admin
    password = knock

    [actions]
    git pull --rebase 