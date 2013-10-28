"""
****************
sloth.validators
****************

Validator collection for Sloth.
"""

def bitbucket(payload, data):
    """Validate Bitbucket payload against repo name and branch (obtained from the Sloth instance config.)

    :param payload: payload to validate
    :param data: dictionary with the keys ``repo`` (in form “username/repo”) and ``branch``

    :returns: (True, success message) of the payload is valid, (False, error message) otherwise
    """

    from json import loads

    try:
        parsed_payload = loads(payload)

        repo = parsed_payload['repository']['owner'] + '/' + parsed_payload['repository']['slug']
        branch = parsed_payload['commits'][-1]['branch']

        if repo == data['repo'] and branch == data['branch']:
            return (True, 'Payload validated')
        elif repo != data['repo']:
            return (False, 'Payload validation failed: repo mismatch')
        elif branch != data['branch']:
            return (False, 'Payload validation failed: branch mismatch')
    except:
        return (False, 'Payload validation failed')


def dummy(payload, data):
    """Dummy validator.

    :param payload: payload to validate
    :param data: dictionary with the key ``message``
    """

    if payload == data['message']:
        return (True, 'Payload validated')
    else:
        return (False, 'Payload validation failed')

validate = {
    'dummy': dummy,
    'bitbucket': bitbucket
}
