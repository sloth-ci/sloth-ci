********
HTTP API
********

The root listen point (``/``) of a Sloth CI server is reserved for the API.

The API listen point expects API requests, which are ordinary HTTP requests with a mandatory ``action`` and numerous optional or mandatory params depending on the action. It doesn't matter if the request is sent via GET or POST—Sloth CI will chew it all. 

The API returns data in the JSON format.

A GET API request looks like this::

    http://host:port/?action=some_action&param1=value1&param2=value2...

The API is protected with basic auth to avoid unwanted access from the outside world. The basic auth credentials are stored in the ``login`` and ``password`` params of the ``api_auth`` section in the :ref:`server config <server-config>`.

.. note::

    Sloth CI's API is not RESTful in any way, it is neither possible or desirable to use this concept with this software.

Below is the full list of available API actions with params and possible return statuses.

``bind``
========

Bind an app with a config file.

GET URL example::

    http://localhost:8080/?action=bind&listen_point=foo&config_file=%2Fhome%2Fbar.yml

Params
------

-   ``action`` = ``bind``
-   ``listen_point`` is a listen point of the app
-   ``config_file`` is an absolute path to the config file

Response
--------

Status **200** with empty content.

Errors
------

-   **404**: no app found on the requested listen point or no file found on the given path (read the error message for details)
-   **500**: config in the file is different from the one used by the app or something unexpected happened in the server (read the error message for details)

``create``
==========

Create a Sloth CI app with a particular configuration. The configuration is specified as a string. Refer to the :ref:`app config <app-config>` description.

GET URL example::
    
    http://localhost:8080/?action=create&config_string=listen_point%3A+test%0D%0A%0D%0A...

Params
------

-   ``action`` = ``create``
-   ``config_string`` is a YAML config string. If you are providing the config string in a GET query, **it must be urlencoded**.

Response
--------

Status **201** with the new app's listen point in the content.

Errors
------

-   **400**: the ``config_string`` param is missing
-   **409**: the requested listen point is already taken
-   **500**: 

    -   invalid config string
    -   config is missing a mandatory param
    -   something unexpected happened on the server

``remove``
==========

Remove a Sloth CI app on a particular listen point.

GET URL example::
    
    http://localhost:8080/?action=remove&listen_point=test

Params
------

-   ``action`` = ``remove``
-   ``listen_point`` is the listen point of the app to be removed.

Response
--------

Status **204** with empty content.

Errors
------

-   **400**: the ``listen_point`` param is missing
-   **404**: no app found on the requested listen point
-   **500**: something unexpected happened in the server (read the error message for details)

``trigger``
===========

Trigger the app's actions execution with a particular set of params. 

.. important:: 

    This command *triggers*, not *executes* the actions. Its call is considered successful it the action execution was successfully trigerred, not necessarily if all the action were successfully executed. You should check the execution success in the app's logs.

GET URL example::

    http://localhost:8080/?action=trigger&listen_point=test&spam=eggs

Params
------

-   ``action`` = ``trigger``
-   ``listen_point`` is the listen point of the app whose actions you want to trigger.
-   params referred to in the actions. You *must* provide the params that would otherwise come from a payload, and you *can* override the params in the :ref:`app config <app-config>`'s ``params`` section.

Response
--------

Status **202** with empty content.

Errors
------

-   **400**: the ``listen_point`` param is missing
-   **404**: no app found on the requested listen point
-   **500**: something unexpected happened in the server (read the error message for details)

``info``
========

Get information about certain or all apps.

GET URL example::

    http://localhost:8080/?action=info&listen_points=spam&listen_points=eggs

Params
------

-   ``action`` = ``info``
-   ``listen_points`` is a list of listen points of the apps. You can pass zero, one, or multiple listen points.

Response
--------

Status **200** with a list of JSON objects like ``{"listen_point": "foo", "config_file": "/home/bar.yml", "last_build_status": "Compete (2/3)", "last_build_timestamp": 12345.67    }``.

Errors
------

-   **404**: no app found on the requested listen point
-   **500**: something unexpected happened in the server (read the error message for details)

``logs``
========

Get paginated app logs. Logs are returned as a sorted by timestamp list, the freshest logs are on top.

.. important::

    App logs are taken from the database, so the ``paths: db`` parameter **must** be set in the server config for this method to work. If you set the ``paths: db`` parameter to ``null``, this method **will be unavailable**.

GET URL example::

    http://localhost:8080/?action=logs&listen_point=spam&from_page=2&per_page=20&level=40

Params
------

-   ``action`` = ``logs``
-   ``listen_point`` is the listen point of the app whose logs you want to get.
-   ``from_page`` is the number of the first page to get. Default is 1 (the first page, i.e. the latest logs).
-   ``to_page`` is the number of the last page to get. Default is ``from_page`` (i.e. get only one page).
-   ``per_page`` is the number of records per page. Default is 10.
-   ``level`` is the numeric value of the minimal record level to be shown. Refer to the `Logging levels <https://docs.python.org/3.4/library/logging.html#levels>`_ table.


Response
--------

Status **200** with a list of JSON objects like ``{"timestamp": 123456.789, "logger_name": "spam.processing", "level_name": "INFO", "level_number": 20, "message": "Execution queue is empty"}``.

Errors
------

-   **500**: something unexpected happened in the server (read the error message for details)

``history``
===========

Get paginated app build history logs. History is returned as a sorted by timestamp list, the freshest statuses are on top.

.. important::

    Build history is taken from the database, so the ``paths: db`` parameter **must** be set in the server config for this method to work. If you set the ``paths: db`` parameter to ``null``, this method **will be unavailable**.

GET URL example::

    http://localhost:8080/?action=history&listen_point=spam&from_page=2&per_page=20

Params
------

-   ``action`` = ``history``
-   ``listen_point`` is the listen point of the app whose build history you want to get.
-   ``from_page`` is the number of the first page to get. Default is 1 (the first page, i.e. the latest statuses).
-   ``to_page`` is the number of the last page to get. Default is ``from_page`` (i.e. get only one page).
-   ``per_page`` is the number of records per page. Default is 10.

Response
--------

Status **200** with a list of JSON objects like ``{"timestamp": 123456.789, "logger_name": "spam.build", "level_name": "INFO", "level_number": 20, "message": "Complete (2/3)"}``.

Errors
------

-   **500**: something unexpected happened in the server (read the error message for details)

``restart``
===========

Ask a Sloth CI server to restart.

.. important::

    This command only *asks* for a restart, it can't guarantee that the server will restart immediatelly or ever at all. You should check the restart success in the server's logs.

GET URL example::
    
        http://localhost:8080/?action=restart

Params
------

-   ``action`` = ``restart``

Response
--------

Status **202** with empty content.

Errors
------

-   **500**: something unexpected happened in the server (read the error message for details)

``stop``
========

Ask a Sloth CI server to stop.

.. important::

    This command only *asks* for a stop, it can't guarantee that the server will stop immediatelly or ever at all. You should check the stop success in the server's logs.

GET URL example::
    
        http://localhost:8080/?action=stop

Params
------

-   ``action`` = ``stop``

Response
--------

Status **202** with empty content.

Errors
------

-   **500**: something unexpected happened in the server (read the error message for details)