********
HTTP API
********

The root listen point (``/``) of a Sloth CI server is reserved for the API. The API is the only way to manage Sloth CI apps and server; even the :doc:`CLI <cli>` works via the HTTP API (except for the ``start`` command, obviously).

The API listen point expects API requests, which are ordinary HTTP requests with a mandatory ``action`` and numerous optional or mandatory params depending on the action. It doesn't matter if the request is sent via GET or POST, if the data is form data, JSON-dictionary, or a GET query—Sloth CI will chew it all. 

A GET API request looks like this::

    http://host:port/?action=some_action&param1=value1&param2=value2...

The API is protected with basic auth to avoid unwanted access from the outside world. The basic auth credentials are stored in the ``login`` and ``password`` params of the ``api_auth`` section in the :ref:`server config <server-config>`.

.. note::

    Sloth CI's API is not RESTful in any way, it is neither possible or desirable to use this concept with this software.

Below is the full list of available API actions with params and possible return statuses.

``create``
==========

Create a Sloth CI app with a particular configuration. The configuration is specified either as a path to a YAML file or as a string. Refer to the :ref:`app config <app-config>` description.

GET URL example::
    
    http://localhost:8080/?action=create&config_source=listen_point%3A+test%0D%0A%0D%0A...

Params
------

-   ``action`` = ``create``
-   ``config_source`` is a path to the config file or a config string. If you are providing a config string in a GET query, **it must be urlencoded**.

Response
--------

Status **201** with the new app's listen point in the content.

Errors
------

-   **400**: the ``config_source`` param is missing
-   **409**: the requested listen point is already taken
-   **500**: either the config source has some mandatory param missing, or something unexpected happened in the server (read the error message for details)

``remove``
==========

Remove a Sloth CI app on a particular listen point.

GET URL example::
    
    http://localhost:8080/?action=remove&listen_point=test

Params
------

-   ``action`` = ``remove``
-   ``listen_point`` is the listen point of the app to be removed.'

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