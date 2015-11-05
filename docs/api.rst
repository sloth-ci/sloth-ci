*************
API Reference
*************

Sloth CI's API lets you stop and restart the server, create and remove apps, and view app logs and build history.

The API is protected from unauthorized access with basic auth; the access credentials are stored in the :ref:`server config <server-config-api-auth>`.

There're three ways to use the API:

-   Using Sloth CI's :doc:`CLI <cli>`:

    .. code-block:: bash

        $ sci info test
        Config File        Last Build Message    Last Build Timestamp
        -----------------  --------------------  ------------------------
        /path/to/test.yml  Completed 2/2         Thu Nov  5 00:47:52 2015


-   By sending GET requests with URL parameters [#httpie]_:

    .. code-block:: bash

        $ http -a admin:password localhost:8080 action==info listen_point==test
        HTTP/1.1 200 OK
        Content-Length: 187
        Content-Type: application/json
        Date: Wed, 04 Nov 2015 21:49:54 GMT
        Server: CherryPy/3.8.0

        {
            "config_file": "/path/to/test.yml",
            "last_build_status_level": "INFO",
            "last_build_status_message": "Completed 2/2",
            "last_build_timestamp": 1446673672.939748
        }

-   By sending POST requests with parameters as form data:

    .. code-block:: bash

        $ http -a admin:password -f POST localhost:8080 action=info listen_point=test
        HTTP/1.1 200 OK
        Content-Length: 187
        Content-Type: application/json
        Date: Wed, 04 Nov 2015 21:50:50 GMT
        Server: CherryPy/3.8.0

        {
            "config_file": "/path/to/test.yml",
            "last_build_status_level": "INFO",
            "last_build_status_message": "Completed 2/2",
            "last_build_timestamp": 1446673672.939748
        }

.. _api-bind:

bind
====



.. rubric:: Footnotes

.. [#httpie] In the code samples, we use `httpie <https://httpie.org>`__—a curl-like HTTP client. It's fantastic, you should try it.
