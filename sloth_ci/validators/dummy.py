def validate(request, validation_data):
    """Dummy validator.

    :param request_params: payload to validate
    :param validation_data: dictionary with the key ``message``
    """

    if request.method != 'GET':
        return (False, 'Payload validation failed: Wrong method, GET expected, got {method}.', {'method': request.method})

    message = request.params.get('message')

    valid_message = validation_data.get('message')

    if message and message == valid_message:
        return (True, 'Payload validated. Message: {message}', {'message': message})
    else:
        return (False, 'Payload validation failed. Message: {message}', {'message': message})
