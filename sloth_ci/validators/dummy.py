def validate(request, validation_data):
    """Dummy validator.

    :param request_params: payload to validate
    :param validation_data: dictionary with the key ``message``
    """

    if request.method != 'GET':
        return (False, 'Payload validation failed: Wrong method, GET expected, got {method}.', {'method': request.method})

    message = request.params.get('message')

    if message == validation_data['message']:
        return (True, 'Payload validated. Message: {message}', {'message': message})
    else:
        return (False, 'Payload validation failed. Message: {message}', {'message': message})