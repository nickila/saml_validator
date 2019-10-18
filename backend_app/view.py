from flask import render_template, request, jsonify, Blueprint

from backend_app.process_error import ErrorHandler
from backend_app.process_request import RequestHandler

view = Blueprint('view', __name__, url_prefix='')


@view.route('/')
def welcome():
    return render_template('index.html')


@view.route('/upload', methods=['POST'])
def upload():
    try:
        return jsonify(RequestHandler.process_request(request))
    except AssertionError as e:
        return jsonify(ErrorHandler.process_error(e))
