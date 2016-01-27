from flask import jsonify
from exceptions import ValidationError
from views import api
from facebook import GraphAPIError

def bad_request(message, status_code=400):
    response = jsonify({'error': 'bad request', 'message': message})
    response.status_code = status_code
    return response

def graph_api_error_response(e):
    return bad_request(e.message)

@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])

@api.errorhandler(GraphAPIError)
def graph_api_error(e):
    return graph_api_error_response(e)
