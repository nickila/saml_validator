from flask import render_template, request, jsonify, Blueprint
from backend_app.process_error import ApiError
from backend_app.process_request import RequestHandler, XMLParsingError

view = Blueprint('view', __name__, url_prefix='')


@view.route('/')
def welcome():
    return render_template('index.html')


@view.route('/upload', methods=['POST'])
def upload():
    try:
        return jsonify(RequestHandler.process_request(request))
    except XMLParsingError as e:
        raise ApiError(status_code=400, error=e, message="XML error")
    except Exception as e:
        raise ApiError(status_code=500, error=e, message=str(e))


@view.errorhandler(ApiError)
def handle_error(error):
    response = jsonify(error.serialize())
    response.status_code = error.status_code
    return response
