from flask import render_template, request, jsonify, Blueprint
from backend_app.error_handler import ApiError, XMLParsingError, SamlParsingError, FileUploadError
from backend_app.request_handler import RequestHandler

view = Blueprint('view', __name__, url_prefix='')


@view.route('/')
def welcome():
    return render_template('index.html')


@view.route('/upload', methods=['POST'])
def upload():
    try:
        return jsonify(RequestHandler.process_request(request))
    except (XMLParsingError, SamlParsingError, FileUploadError) as e:
        raise ApiError(status_code=400, error=e)
    except Exception as e:
        raise ApiError(status_code=400, error=e, message=str(e))


@view.errorhandler(ApiError)
def handle_error(error):
    response = jsonify(error.serialize())
    response.status_code = error.status_code
    return response
