def validate(request_params, validation_data):
    """Validate Bitbucket payload against repo name (obtained from the Sloth instance config).

    :param request_params: payload to validate
    :param validation_data: dictionary with the key ``repo`` (in the form "username/repo")

    :returns: (True, success message, extracted data dict) of the payload is valid, (False, error message, extracted data dict) otherwise
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