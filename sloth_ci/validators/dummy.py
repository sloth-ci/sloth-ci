def validate(request_params, validation_data):
    """Dummy validator.

    :param request_params: payload to validate
    :param validation_data: dictionary with the key ``message``
    """

    message = request_params.get('message')

    if message == validation_data['message']:
        return (True, 'Payload validated. Message: {message}', {'message': message})
    else:
        return (False, 'Payload validation failed. Message: {message}', {'message': message})