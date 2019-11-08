import pytest
import flask
from flask import Request
import os
from unittest.mock import MagicMock

from werkzeug.datastructures import FileStorage

from backend_app.request_handler import RequestHandler

def test_process_request():
    with open('fixtures/saml_trace.xml') as xml:
        file = FileStorage(content_type='application/xml', name='saml_file', stream=xml)
        request = MagicMock()
        request.files = {'saml_file': file}
        request.data.return_value = {'idp_name': None}
        result = RequestHandler.process_request(request)
        print()
