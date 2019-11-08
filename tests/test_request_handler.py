import pytest
import flask
from flask import Request
import os
from unittest.mock import MagicMock

from werkzeug.datastructures import FileStorage

from backend_app.request_handler import RequestHandler


def test_process_request(descriptions, idp_repo, stub_response):
    RequestHandler.idp_repo = idp_repo
    RequestHandler.descriptions = descriptions
    with open('fixtures/saml_trace.xml') as xml:
        file = FileStorage(content_type='application/xml', name='saml_file', stream=xml)
        request = MagicMock()
        request.files = {'saml_file': file}
        request.values = {'idp_name': 'Other'}
        result = RequestHandler.process_request(request)

    assert result == stub_response


@pytest.fixture
def stub_response():
    return {'assertion_attributes': {
        'value': {'LastName': 'example_last_name', 'FirstName': 'example_first_name', 'Email': 'email@example.edu',
                  'Other': 'other attribute'}, 'description': 'Attributes included in your SAML assertion'},
            'name_id': {'value': '22334384CCCCE66c123',
                        'description': 'Name-ID attribute, format of attribute must match your login setting of your federated directory'},
            'name_id_format': {'value': 'urn:oasis:names:tc:SAML:2.0:nameid-format:emailAddress',
                               'description': 'Format of your Name-ID attribute'},
            'destination': {'value': 'https://https://adobe-location-from_meta',
                            'description': 'Must match Location attribute value from Adobe Metadata'},
            'issuer_url': {'value': 'https://https://adobe-entity-id',
                           'description': 'Must match Entity ID attribute value from Adobe Metadata'},
            'signature_method_algorithm': {'value': 'https://www.w3.org/2000/09/xmldsig#rsa-sha1',
                                           'description': 'Should be rsa-sha1'},
            'digest_method_algorithm': {'value': 'https://www.w3.org/2000/09/xmldsig#rsa-sha1',
                                        'description': 'Should be rsa-sha1'},
            'not_before': {'value': '2019-08-21T18:30:58Z'}, 'time_sent': {'value': '2019-08-21T18:36:29Z',
                                                                           'description': "Timestamp must be within the 'not_before' and 'not_on_or_after' time window"},
            'not_on_or_after': {'value': '2019-08-21T18:36:28Z'}, 'signing_cert': {'value': 'MIIEA_signing_cert_saml',
                                                                                   'description': 'Token-Signing Certificate, must be Base-64 encoded X.509(.CER), which is equivalent to a PEM format certificate'},
            'in_response_to': {'value': 'id18283838494959494949'}}
