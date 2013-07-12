"""
****************
sloth.validators
****************

Validator collection for Sloth.
"""

def bitbucket(payload, config):
    """Validate Bitbucket payload against repo name and branch (obtained from the Sloth instance config.)

    :param payload: payload to be validated

    :returns: (True, success message) of the payload is valid, (False, error message) otherwise
    """

    from json import loads

    if payload == 'test':
        return (True, 'Payload validated')

    try:
        parsed_payload = loads(payload)

        repo = parsed_payload['repository']['owner'] + '/' + parsed_payload['repository']['slug']
        branch = parsed_payload['commits'][-1]['branch']

        if repo == config['repo'] and branch == config['branch']:
            return (True, 'Payload validated')
        elif repo != config['repo']:
            return (False, 'Payload validation failed: repo mismatch')
        elif branch != config['branch']:
            return (False, 'Payload validation failed: branch mismatch')
    except:
        return (False, 'Payload validation failed')

validate = {
    'bitbucket': bitbucket
}
