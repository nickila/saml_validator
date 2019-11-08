from backend_app.response_builder import ResponseBuilder


def test_construct_response(saml_parsed_dict, descriptions):
    errors = {'assertion_attributes': {'description': 'Assertion must include FirstName, LastName, and Email'},
              'name_id': {'descriptions': 'Name-ID attribute must be present with unspecified or emailAddress format'},
              'name_id_format': {'description': 'Name-ID requires unspecified or emailAddress format'},
              'signing_cert': {'description': 'Signing cert not present'}}

    result = ResponseBuilder.construct_response(saml_parsed_dict, descriptions, errors)
    expected = {'assertion_attributes': {
        'value': {'LastName': 'example_last_name', 'FirstName': 'example_first_name', 'Email': 'email@example.edu',
                  'Other': 'other attribute'},
        'errors_found': {'description': 'Assertion must include FirstName, LastName, and Email'}},
                'name_id': {'value': '22334384CCCCE66c123', 'errors_found': {
                    'descriptions': 'Name-ID attribute must be present with unspecified or emailAddress format'}},
                'name_id_format': {'value': 'urn:oasis:names:tc:SAML:2.0:nameid-format:emailAddress', 'errors_found': {
                    'description': 'Name-ID requires unspecified or emailAddress format'}},
                'destination': {'value': 'https://https://adobe-location-from_meta'},
                'issuer_url': {'value': 'https://https://adobe-entity-id'},
                'signature_method_algorithm': {'value': 'https://www.w3.org/2000/09/xmldsig#rsa-sha1'},
                'digest_method_algorithm': {'value': 'https://www.w3.org/2000/09/xmldsig#rsa-sha1'},
                'not_before': {'value': '2019-08-21T18:30:58Z'}, 'time_sent': {'value': '2019-08-21T18:36:29Z'},
                'not_on_or_after': {'value': '2019-08-21T18:36:28Z'},
                'signing_cert': {'value': 'MIIEA_signing_cert_saml',
                                 'errors_found': {'description': 'Signing cert not present'}},
                'in_response_to': {'value': 'id18283838494959494949'}}
    assert result == expected
