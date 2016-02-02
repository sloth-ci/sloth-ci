'''Describe your validator.

Installation
------------

.. code-block:: bash

    $ pip install sloth-ci.validators.myvalidator


Usage
-----

.. code-block:: yaml

    provider:
        myvalidator:
            param1: value1
            param2: value2
            ...
'''


__title__ = 'sloth-ci.validators.myvalidator'
__description__ = 'Describe your validator'
__version__ = '0.0.1'
__author__ = 'Your Name'
__author_email__ = 'your@email.com'
__license__ = 'MIT'


def validate(request, validation_data):
    '''Validate incoming payload.

    :param request: `CherryPy request <http://docs.cherrypy.org/en/latest/pkg/cherrypy.html#cherrypy._cprequest.Request>`_ instance representing incoming request
    :param validation_data: dict with validation data, e.g. ``owner``, ``repo``, ``branches``, extracted from the app config

    :returns: namedtuple(status, message, list of extracted params as dicts), e.g. ``Response(status=200, message='Payload validated. Branches: default', [{'branch': 'default'}])``
    '''

    from collections import namedtuple


    Response = namedtuple('Response', ('status', 'message', 'param_dicts'))

    return Response(200, 'Payload validated. Branches: default', [{'branch': 'default'}])
