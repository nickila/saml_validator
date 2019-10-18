#from backend_app.app import app
import backend_app.app
from flask import render_template, request, jsonify
from backend_app.process_request import RequestHandler
from backend_app.process_error import ErrorHandler


@backend_app.app.my_app.route('/')
def welcome():
    return render_template('index.html')


@backend_app.app.my_app.route('/upload', methods=['POST'])
def upload():
    try:
        return jsonify(RequestHandler.process_request(request))
    except AssertionError as e:
        return jsonify(ErrorHandler.process_error(e))
