def validate(payload, data):
    """Dummy validator.

    :param payload: payload to validate
    :param data: dictionary with the key ``message``
    """

    if payload == data['message']:
        return (True, 'Payload validated')
    else:
        return (False, 'Payload validation failed')