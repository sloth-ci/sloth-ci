def validate(payload, data):
    """Validate Bitbucket payload against repo name (obtained from the Sloth instance config).

    :param payload: payload to validate
    :param data: dictionary with the keys ``repo`` (in the form "username/repo") and ``branch``

    :returns: (True, success message) of the payload is valid, (False, error message) otherwise
    """

    from json import loads

    try:
        parsed_payload = loads(payload)

        repo = parsed_payload['repository']['owner'] + '/' + parsed_payload['repository']['slug']
        branch = parsed_payload['commits'][-1]['branch']

        if repo != data['repo']:
            return (False, 'Payload validation failed: repo mismatch. Repo: {repo}', {'repo': repo})
        
        return (True, 'Payload validated. Branch: {branch}', {'branch': branch})
    
    except Exception as e:
        return (False, 'Payload validation failed: %s' % e, {})