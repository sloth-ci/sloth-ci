.. highlight:: bash


***
API
***

Sloth CI's API lets you stop and restart the server, create and remove apps, list app logs and view app build history.

The API runs on the host and port specified in the :ref:`server config <server-config-host>`. It's protected from unauthorized access with basic auth; the access credentials are also stored in the :ref:`server config <server-config-api-auth>`.

The API returned data in JSON format.

There're three ways to call an :ref:`API method <api-methods>`:

-  Use Sloth CI's :doc:`CLI <cli>`::

        $ sci info test
        Config File        Last Build Message   Last Build Timestamp
        -----------------  -------------------  ------------------------
        /path/to/test.yml  Completed 2/2        Thu Nov  5 00:47:52 2015

-   Visit ``http://example.com:8080/?action=info&listen_point=test``

-   Send POST requests with form parameters [#httpie]_::

        $ http -f -a login:password localhost:8080 \
            action=info \
            listen_point=test
        HTTP/1.1 200 OK
        Content-Length: 193
        Content-Type: application/json
        Date: Fri, 27 Nov 2015 21:37:15 GMT
        Server: CherryPy/3.8.0

        {
            "config_file": "C:\\Users\\moigagoo\\Projects\\sloth-ci\\test.yml",
            "last_build_status_level": "INFO",
            "last_build_status_message": "Completed 2/2",
            "last_build_timestamp": 1446414114.7911112
        }


.. _api-methods:

Methods
=======

.. _api-create:

create
------

Create an app from the given config string::

    $ http -f -a login:password localhost:8080 \
            action=create \
            config_string=$(cat test.yml)
    HTTP/1.1 201 Created
    Content-Length: 6
    Content-Type: application/json
    Date: Fri, 27 Nov 2015 21:39:58 GMT
    Server: CherryPy/3.8.0

    "test"

``config_string``
    URL-encoded :doc:`app config <app-config>`.


.. _api-bind:

bind
----

If the app is :ref:`created <api-create>` from a config file, bind them together, so Sloth CI would know where to read the config from when you :ref:`reload <cli-reload>` the app::

    $ http -f -a login:password localhost:8080 \
            action=bind \
            listen_point=test \
            config_file=/path/to/test.yml
    HTTP/1.1 200 OK
    Content-Length: 4
    Content-Type: application/json
    Date: Fri, 27 Nov 2015 21:41:24 GMT
    Server: CherryPy/3.8.0

    null

``listen_point``
    App listen point.

``config_file``
    Path to the config file ti bind with the app.

The :ref:`create <cli-create>` CLI command  runs the :ref:`create <api-create>` and :ref:`bind <api-bind>` API methods.


.. _api-trigger:

trigger
-------

Trigger app's actions::

    $ http -f -a login:password localhost:8080 \
            action=trigger \
            listen_point=test \
            foo=bar
    HTTP/1.1 202 Accepted
    Content-Length: 4
    Content-Type: application/json
    Date: Sat, 28 Nov 2015 07:17:42 GMT
    Server: CherryPy/3.8.0

    null

Trigger app's actions and wait for them to complete::

    $ http -f -a login:password localhost:8080 \
            action=trigger \
            listen_point=test \
            wait=true \
            foo=bar
    HTTP/1.1 200 OK
    Content-Length: 15
    Content-Type: application/json
    Date: Sat, 28 Nov 2015 07:19:40 GMT
    Server: CherryPy/3.8.0

    "Completed 2/2"

``listen_point``
    App listen point.

``wait`` *optional*
    Wait for the actions to complete.

custom params *optional*
    Any number of params to replace :ref:`placeholders <app-config-placeholders>` in the actions.


.. _api-info:

info
----

Get app config file path and last build status::

    $ http -f -a login:password localhost:8080 \
            action=trigger \
            listen_point=test
    HTTP/1.1 200 OK
    Content-Length: 192
    Content-Type: application/json
    Date: Sat, 28 Nov 2015 07:53:18 GMT
    Server: CherryPy/3.8.0

    {
        "config_file": "C:\\Users\\moigagoo\\Projects\\sloth-ci\\test.yml",
        "last_build_status_level": "INFO",
        "last_build_status_message": "Completed 2/2",
        "last_build_timestamp": 1448695186.978541
    }


.. _api-history:

history
-------

Get app build history::

    $ http -f -a login:password localhost:8080 \
            action=history \
            listen_point=test
    HTTP/1.1 200 OK
    Content-Length: 1422
    Content-Type: application/json
    Date: Sat, 28 Nov 2015 07:56:56 GMT
    Server: CherryPy/3.8.0

    [
        {
            "level_name": "INFO",
            "level_number": 20,
            "logger_name": "test.build",
            "message": "Completed 2/2",
            "timestamp": 1448695186.978541
        },
        ...

Paginate and filter by status::

    $ http -f -a login:password localhost:8080 \
            action=list \
            listen_point=test \
            from_page=3 \
            per_page=2 \
            level=10
    HTTP/1.1 200 OK
    Content-Length: 1422
    Content-Type: application/json
    Date: Sat, 28 Nov 2015 07:56:56 GMT
    Server: CherryPy/3.8.0

    [
        {
            "level_name": "INFO",
            "level_number": 20,
            "logger_name": "test.exec",
            "message": "Executing action: PowerShell echo Good morning!",
            "timestamp": 1448695185.3463366
        },
        ...

``listen_point``
    App listen point.

``from_page``, ``to_page``, ``per_page``
    Pagination params.

    By default, ``from_page`` = 1, ``to_page`` = ``from_page``, ``per_page`` = 10.

``level``
    Minimal log level to show:

    40
        ERROR, failed builds.

    30
        WARNING, partially completed builds.

    20 (default)
        INFO, completed builds.

    10
        DEBUG, trigger events.


.. _api-logs:

logs
----

Get app logs::

    $ http -f -a login:password localhost:8080 \
            action=logs \
            listen_point=test
    HTTP/1.1 200 OK
    Content-Length: 1422
    Content-Type: application/json
    Date: Sat, 28 Nov 2015 07:56:56 GMT
    Server: CherryPy/3.8.0

    [
        {
            "level_name": "INFO",
            "level_number": 20,
            "logger_name": "test.build",
            "message": "Completed 2/2",
            "timestamp": 1448695186.978541
        },
        ...

Paginate and filter by log level::

    $ http -f -a login:password localhost:8080 \
            action=logs \
            listen_point=test \
            from_page=3 \
            per_page=2 \
            level=10
    HTTP/1.1 200 OK
    Content-Length: 1422
    Content-Type: application/json
    Date: Sat, 28 Nov 2015 07:56:56 GMT
    Server: CherryPy/3.8.0

    [
        {
            "level_name": "INFO",
            "level_number": 20,
            "logger_name": "test.exec",
            "message": "Executing action: PowerShell echo Good morning!",
            "timestamp": 1448695185.3463366
        },
        ...

``listen_point``
    App listen point.

``from_page``, ``to_page``, ``per_page``
    Pagination params.

    By default, ``from_page`` = 1, ``to_page`` = ``from_page``, ``per_page`` = 10.

``level``
    Minimal log level to show:

    50
        CRITICAL, errors that don't allow apps to be created, e.g missing validator.

    40
        ERROR, missing extension and failed builds.

    30
        WARNING, partially completed builds.

    20 (default)
        INFO, completed builds.

    10
        DEBUG, stdout and stderr.


.. _api-list:

list
----

List existing app listen points::

    $ http -f -a login:password localhost:8080 \
            action=list
    HTTP/1.1 200 OK
    Content-Length: 8
    Content-Type: application/json
    Date: Sat, 28 Nov 2015 07:55:26 GMT
    Server: CherryPy/3.8.0

    [
        "test"
    ]


.. _api-remove:

remove
------

Remove the app::

    $ http -f -a login:password localhost:8080 \
            action=remove \
            listen_point=test
    HTTP/1.1 204 No Content
    Content-Type: application/json
    Date: Fri, 27 Nov 2015 21:43:41 GMT
    Server: CherryPy/3.8.0


.. _api-version:

version
-------

Get the version of the Sloth CI server::

    $ http -f -a login:password localhost:8080 \
            action=version
    HTTP/1.1 200 OK
    Content-Length: 7
    Content-Type: application/json
    Date: Sun, 29 Nov 2015 10:11:08 GMT
    Server: CherryPy/3.8.0

    "2.0.1"


.. _api-restart:

restart
-------

Restart the Sloth CI server::

    $ http -f -a login:password localhost:8080 \
            action=restart
    HTTP/1.1 202 Accepted
    Content-Length: 4
    Content-Type: application/json
    Date: Sun, 29 Nov 2015 10:14:39 GMT
    Server: CherryPy/3.8.0

    null


.. _api-stop:

stop
----

Stop the Sloth CI server::

    $ http -f -a login:password localhost:8080 \
            action=stop
    HTTP/1.1 202 Accepted
    Content-Length: 4
    Content-Type: application/json
    Date: Sun, 29 Nov 2015 10:14:39 GMT
    Server: CherryPy/3.8.0

    null


.. rubric:: Footnotes

.. [#httpie] In the examples, HTTP requests are sent with `httpie <http://httpie.org>`__.