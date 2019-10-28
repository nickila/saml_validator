import pytest
from collections import OrderedDict
from backend_app.analyzer import Analyzer
from backend_app.error_handler import XMLParsingError, SamlParsingError

from backend_app.saml_result import SamlResult


def test_parse_saml(saml_file_dict, saml2_file_dict, saml_parsed_dict, saml2_parsed_dict):
    result = Analyzer.parse_saml(saml_file_dict)
    expected = saml_parsed_dict
    assert result == expected

    # testing saml2 key
    result = Analyzer.parse_saml(saml2_file_dict)
    expected = saml2_parsed_dict
    assert result == expected

    # asserts SamlParsingError exception is thrown when no saml values are found
    with pytest.raises(SamlParsingError):
        Analyzer.parse_saml({'saml3p': {}})


def test_construct_result(saml_parsed_dict, descriptions):
    errors = {'assertion_attributes': {'description': 'Assertion must include FirstName, LastName, and Email'},
              'name_id': {'descriptions': 'Name-ID attribute must be present with unspecified or emailAddress format'},
              'name_id_format': {'description': 'Name-ID requires unspecified or emailAddress format'},
              'signing_cert': {'description': 'Signing cert not present'}}

    result = SamlResult.construct_result(saml_parsed_dict, descriptions, errors)
    expected = {'assertion_attributes': {
        'value': {'LastName': 'user_lastname', 'FirstName': 'user_firstname', 'Email': 'user_email@example.com',
                  'Other': 'other attribute'},
        'errors_found': {'description': 'Assertion must include FirstName, LastName, and Email'}},
                'name_id': {'value': 'user_email@example.com', 'errors_found': {
                    'descriptions': 'Name-ID attribute must be present with unspecified or emailAddress format'}},
                'name_id_format': {'value': 'urn:oasis:names:tc:SAML:2.0:nameid-format:emailAddress', 'errors_found': {
                    'description': 'Name-ID requires unspecified or emailAddress format'}},
                'destination': {'value': 'https://https://adobe-location-from_meta'},
                'issuer_url': {'value': 'https://https://adobe-entity-id'},
                'signature_method_algorithm': {'value': 'https://www.w3.org/2000/09/xmldsig#rsa-sha1'},
                'digest_method_algorithm': {'value': 'https://www.w3.org/2000/09/xmldsig#rsa-sha1'},
                'not_before': {'value': '2019-08-21T18:30:58Z'}, 'time_sent': {'value': '2019-08-21T18:36:29Z'},
                'not_on_or_after': {'value': '2019-08-21T18:36:28Z'},
                'signing_cert': {'value': 'MIIEA..saml..signing..cert..M=',
                                 'errors_found': {'description': 'Signing cert not present'}}}
    assert result == expected


def test_create_error_dict(saml_parsed_dict, descriptions, idp_repo):
    # checks compatibility with all idp options
    for each in {'google', 'adfs', 'shibboleth', 'azure', 'okta', 'wso2'}:
        result = Analyzer.create_error_dict(saml_parsed_dict, descriptions.get('error_message'), idp_repo.get(each))
        assert result == {}

    result = Analyzer.create_error_dict(saml_parsed_dict, descriptions.get('error_message'))
    assert result == {}

    saml_parsed_dict['name_id_format'] = 'transient'
    saml_parsed_dict['signing_cert'] = None
    saml_parsed_dict['name_id'] = None
    saml_parsed_dict['assertion_attributes'] = None
    result = Analyzer.create_error_dict(saml_parsed_dict, descriptions.get('error_message'), idp_repo['adfs'])
    assert {'assertion_attributes', 'name_id_format', 'signing_cert'}.issubset(result)

    saml_parsed_dict['assertion_attributes'] = {'astName': 'wrong', 'FirstName': 'right', 'Email': 'right'}
    result = Analyzer.create_error_dict(saml_parsed_dict, descriptions.get('error_message'), idp_repo['adfs'])
    assert 'assertion_attributes' in result


@pytest.fixture
def saml_parsed_dict():
    return {
        'assertion_attributes': {'LastName': 'user_lastname', 'FirstName': 'user_firstname',
                                 'Email': 'user_email@example.com',
                                 'Other': 'other attribute'}, 'name_id': 'user_email@example.com',
        'name_id_format': 'urn:oasis:names:tc:SAML:2.0:nameid-format:emailAddress',
        'destination': 'https://https://adobe-location-from_meta', 'issuer_url': 'https://https://adobe-entity-id',
        'signature_method_algorithm': 'https://www.w3.org/2000/09/xmldsig#rsa-sha1',
        'digest_method_algorithm': 'https://www.w3.org/2000/09/xmldsig#rsa-sha1', 'not_before': '2019-08-21T18:30:58Z',
        'time_sent': '2019-08-21T18:36:29Z', 'not_on_or_after': '2019-08-21T18:36:28Z',
        'signing_cert': 'MIIEA..saml..signing..cert..M='}


@pytest.fixture
def saml2_parsed_dict():
    return {'assertion_attributes': {'FirstName': 'user_firstname', 'LastName': 'user_lastname',
                                     'Email': 'user_email@example.com'},
            'name_id': 'user_email@example.com',
            'name_id_format': 'urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified',
            'destination': 'https://federatedid-na1.services.adobe.com/federated/saml/SSO',
            'issuer_url': 'https://federatedid-na1.services.adobe.com/federated/saml/metadata',
            'signature_method_algorithm': 'http://www.w3.org/2000/09/xmldsig#rsa-sha1',
            'digest_method_algorithm': 'http://www.w3.org/2000/09/xmldsig#sha1',
            'not_before': '2019-10-01T21:19:26.284Z', 'time_sent': '2019-10-01T21:24:26.284Z',
            'not_on_or_after': '2019-10-01T21:29:26.284Z',
            'signing_cert': 'MIIEA..saml2..signing..cert..M='}


@pytest.fixture
def saml_file_dict():
    return OrderedDict([('samlp:Response', OrderedDict([('@Destination', 'https://https://adobe-location-from_meta'),
                                                        ('@ID', '_8007e618625161c6444e4d44f14b93bcc7571c5858'),
                                                        ('@InResponseTo', 'id12571430288981441996829275'),
                                                        ('@IssueInstant', '2019-08-21T18:36:29Z'), ('@Version', '2.0'),
                                                        ('@xmlns:saml', 'urn:oasis:names:tc:SAML:2.0:assertion'),
                                                        ('@xmlns:samlp', 'urn:oasis:names:tc:SAML:2.0:protocol'), (
                                                            'saml:Issuer',
                                                            'https://nam04.safelinks.protection.outlook.com/?url=https%3A%2F%2Fsaml.purchase.edu%2Fsimplesaml%2Fsaml2%2Fidp%2Fmetadata.php&data=02%7C01%7Cper74005%40adobe.com%7Cde0b15077fb54954505808d72665e2b0%7Cfa7b1b5a7b34438794aed2c178decee1%7C0%7C0%7C637020091353487113&sdata=unhMbHx%2B7c3cMQYzrkaFD3RVsncJEM3kRHudEAKAfr8%3D&reserved=0'),
                                                        ('ds:Signature', OrderedDict([('@xmlns:ds',
                                                                                       'https://nam04.safelinks.protection.outlook.com/?url=http%3A%2F%2Fwww.w3.org%2F2000%2F09%2Fxmldsig%23&data=02%7C01%7Cper74005%40adobe.com%7Cde0b15077fb54954505808d72665e2b0%7Cfa7b1b5a7b34438794aed2c178decee1%7C0%7C0%7C637020091353487113&sdata=Eudp%2Fat1NSK9YNMmGCJQeY4lByABBGJhnkSrHqwFrlg%3D&reserved=0'),
                                                                                      ('ds:SignedInfo', OrderedDict([(
                                                                                          'ds:CanonicalizationMethod',
                                                                                          OrderedDict(
                                                                                              [(
                                                                                                  '@Algorithm',
                                                                                                  'https://nam04.safelinks.protection.outlook.com/?url=http%3A%2F%2Fwww.w3.org%2F2001%2F10%2Fxml-exc-c14n%23&data=02%7C01%7Cper74005%40adobe.com%7Cde0b15077fb54954505808d72665e2b0%7Cfa7b1b5a7b34438794aed2c178decee1%7C0%7C0%7C637020091353487113&sdata=4bQtFPOBOrSCgZRCeYAzi0ckBQIgU2JSVqvpeeEZhcQ%3D&reserved=0')])),
                                                                                          (
                                                                                              'ds:SignatureMethod',
                                                                                              OrderedDict(
                                                                                                  [(
                                                                                                      '@Algorithm',
                                                                                                      'https://www.w3.org/2000/09/xmldsig#rsa-sha1')])),
                                                                                          (
                                                                                              'ds:Reference',
                                                                                              OrderedDict(
                                                                                                  [(
                                                                                                      '@URI',
                                                                                                      '#_8007e618625161c6444e4d44f14b93bcc7571c5858'),
                                                                                                      (
                                                                                                          'ds:Transforms',
                                                                                                          OrderedDict(
                                                                                                              [
                                                                                                                  (
                                                                                                                      'ds:Transform',
                                                                                                                      [
                                                                                                                          OrderedDict(
                                                                                                                              [
                                                                                                                                  (
                                                                                                                                      '@Algorithm',
                                                                                                                                      'https://nam04.safelinks.protection.outlook.com/?url=http%3A%2F%2Fwww.w3.org%2F2000%2F09%2Fxmldsig%23enveloped-signature&data=02%7C01%7Cper74005%40adobe.com%7Cde0b15077fb54954505808d72665e2b0%7Cfa7b1b5a7b34438794aed2c178decee1%7C0%7C0%7C637020091353487113&sdata=qvFa9Xyt0CnISl%2BhTL2g%2FQZglJWLzzZy8e0j4ZBQgrE%3D&reserved=0')]),
                                                                                                                          OrderedDict(
                                                                                                                              [
                                                                                                                                  (
                                                                                                                                      '@Algorithm',
                                                                                                                                      'https://nam04.safelinks.protection.outlook.com/?url=http%3A%2F%2Fwww.w3.org%2F2001%2F10%2Fxml-exc-c14n%23&data=02%7C01%7Cper74005%40adobe.com%7Cde0b15077fb54954505808d72665e2b0%7Cfa7b1b5a7b34438794aed2c178decee1%7C0%7C0%7C637020091353487113&sdata=4bQtFPOBOrSCgZRCeYAzi0ckBQIgU2JSVqvpeeEZhcQ%3D&reserved=0')])])])),
                                                                                                      (
                                                                                                          'ds:DigestMethod',
                                                                                                          OrderedDict(
                                                                                                              [
                                                                                                                  (
                                                                                                                      '@Algorithm',
                                                                                                                      'https://www.w3.org/2000/09/xmldsig#rsa-sha1')])),
                                                                                                      (
                                                                                                          'ds:DigestValue',
                                                                                                          'FDRDW5mqPtYzQL4Pv+MhE25R4cY=')]))])),
                                                                                      ('ds:SignatureValue',
                                                                                       'Hd4cH/WcotwGjekGSh2vx8kgAx1wZqPy0zrXU3rSIp7xb2XcwiZ/M5ITKKWTv9nhe+mMs41bB+0vzR9m5tcbsx9samyfje86TtWCcUllFsPWVnHuyfkXOn5m7ZqQZEhYouhhsx1aZwnYZ9W3a5I4aEUWbwKPP45AcuzI7KW95e/IfwJ35FLz82umhAab7aFd03Pb40d+vawjJ2nBubvAUfPE6xk+LauQluy63OXyOiEKAfU16gjBuN28Qc0hAMKuFr5+BjlIH/bDBSNYV2tE87HuxaNBoAtta4GS5yJPotQ33ke2906J00aXCwyThZDSBvYZ91SToSjojiLLdXKgZg=='),
                                                                                      ('ds:KeyInfo', OrderedDict([(
                                                                                          'ds:X509Data',
                                                                                          OrderedDict(
                                                                                              [(
                                                                                                  'ds:X509Certificate',
                                                                                                  'MIIEA..saml..signing..cert..M=')]))]))])),
                                                        ('samlp:Status', OrderedDict([('samlp:StatusCode', OrderedDict(
                                                            [('@Value',
                                                              'urn:oasis:names:tc:SAML:2.0:status:Success')]))])),
                                                        ('saml:Assertion', OrderedDict(
                                                            [('@ID', '_e45bd0729b96af998f30f66311545abdf631dc4c83'),
                                                             ('@IssueInstant', '2019-08-21T18:31:28Z'),
                                                             ('@Version', '2.0'),
                                                             ('@xmlns:xs',
                                                              'https://nam04.safelinks.protection.outlook.com/?url=http%3A%2F%2Fwww.w3.org%2F2001%2FXMLSchema&data=02%7C01%7Cper74005%40adobe.com%7Cde0b15077fb54954505808d72665e2b0%7Cfa7b1b5a7b34438794aed2c178decee1%7C0%7C0%7C637020091353487113&sdata=M1NpAJeO8llLSVZGUK3Q%2F4JTEqhqBJ%2BRqVeXdp%2Bihe0%3D&reserved=0'),
                                                             ('@xmlns:xsi',
                                                              'https://nam04.safelinks.protection.outlook.com/?url=http%3A%2F%2Fwww.w3.org%2F2001%2FXMLSchema-instance&data=02%7C01%7Cper74005%40adobe.com%7Cde0b15077fb54954505808d72665e2b0%7Cfa7b1b5a7b34438794aed2c178decee1%7C0%7C0%7C637020091353487113&sdata=27vJY6qN8rfnhpMdimHb%2FpJbvSrRmN%2F018WdTT%2FWH5I%3D&reserved=0'),
                                                             ('saml:Issuer', 'https://adobe-entity-id'),
                                                             ('ds:Signature',
                                                              OrderedDict([(
                                                                  '@xmlns:ds',
                                                                  'https://nam04.safelinks.protection.outlook.com/?url=http%3A%2F%2Fwww.w3.org%2F2000%2F09%2Fxmldsig%23&data=02%7C01%7Cper74005%40adobe.com%7Cde0b15077fb54954505808d72665e2b0%7Cfa7b1b5a7b34438794aed2c178decee1%7C0%7C0%7C637020091353487113&sdata=Eudp%2Fat1NSK9YNMmGCJQeY4lByABBGJhnkSrHqwFrlg%3D&reserved=0'),
                                                                  (
                                                                      'ds:SignedInfo',
                                                                      OrderedDict(
                                                                          [
                                                                              (
                                                                                  'ds:CanonicalizationMethod',
                                                                                  OrderedDict(
                                                                                      [
                                                                                          (
                                                                                              '@Algorithm',
                                                                                              'https://nam04.safelinks.protection.outlook.com/?url=http%3A%2F%2Fwww.w3.org%2F2001%2F10%2Fxml-exc-c14n%23&data=02%7C01%7Cper74005%40adobe.com%7Cde0b15077fb54954505808d72665e2b0%7Cfa7b1b5a7b34438794aed2c178decee1%7C0%7C0%7C637020091353487113&sdata=4bQtFPOBOrSCgZRCeYAzi0ckBQIgU2JSVqvpeeEZhcQ%3D&reserved=0')])),
                                                                              (
                                                                                  'ds:SignatureMethod',
                                                                                  OrderedDict(
                                                                                      [
                                                                                          (
                                                                                              '@Algorithm',
                                                                                              'https://www.w3.org/2000/09/xmldsig#rsa-sha1')])),
                                                                              (
                                                                                  'ds:Reference',
                                                                                  OrderedDict(
                                                                                      [
                                                                                          (
                                                                                              '@URI',
                                                                                              '#_e45bd0729b96af998f30f66311545abdf631dc4c83'),
                                                                                          (
                                                                                              'ds:Transforms',
                                                                                              OrderedDict(
                                                                                                  [
                                                                                                      (
                                                                                                          'ds:Transform',
                                                                                                          [
                                                                                                              OrderedDict(
                                                                                                                  [
                                                                                                                      (
                                                                                                                          '@Algorithm',
                                                                                                                          'https://nam04.safelinks.protection.outlook.com/?url=http%3A%2F%2Fwww.w3.org%2F2000%2F09%2Fxmldsig%23enveloped-signature&data=02%7C01%7Cper74005%40adobe.com%7Cde0b15077fb54954505808d72665e2b0%7Cfa7b1b5a7b34438794aed2c178decee1%7C0%7C0%7C637020091353497110&sdata=e4JURVlA9yWPldc5JCf%2F1xlseqfMxHv7wI%2F%2FHUDf5JM%3D&reserved=0')]),
                                                                                                              OrderedDict(
                                                                                                                  [
                                                                                                                      (
                                                                                                                          '@Algorithm',
                                                                                                                          'https://nam04.safelinks.protection.outlook.com/?url=http%3A%2F%2Fwww.w3.org%2F2001%2F10%2Fxml-exc-c14n%23&data=02%7C01%7Cper74005%40adobe.com%7Cde0b15077fb54954505808d72665e2b0%7Cfa7b1b5a7b34438794aed2c178decee1%7C0%7C0%7C637020091353497110&sdata=aGuUp1osujSvQjmYfXnJtUmQ4YrptubSHkF8HGBwNzk%3D&reserved=0')])])])),
                                                                                          (
                                                                                              'ds:DigestMethod',
                                                                                              OrderedDict(
                                                                                                  [
                                                                                                      (
                                                                                                          '@Algorithm',
                                                                                                          'https://www.w3.org/2000/09/xmldsig#rsa-sha1')])),
                                                                                          (
                                                                                              'ds:DigestValue',
                                                                                              'MOXAYFO+kXKXwf5qCNPpKByYqE0=')]))])),
                                                                  (
                                                                      'ds:SignatureValue',
                                                                      'HxqM1vsGyN6rqrRhC2h84291k6X/Ef0A5CqaptrjYmS5llvAvI+nmqK06rEm8mnKAZVDzrwleCzQiZSwo/t5Xmwc+bilgBXUWjK0ccrbPBZ82Do2hrapugVO0/Z26aygi6kp/CEB0NfU5632RYL7xS2MkOwuYvrn0DVkHlJZdbtt/GXoUZFojDiM+m7YzDljSZq6bYAgJsn4pK8se2CAM8rmD05EvHiAbV1ZLF3sgYxsZJqfWadpvAV0uIpVmuqUp6WGMT6OiEQJuDWPdkpl9vDqAxiDcBf55NUw7OypU3hQCQLTx9AcOLtMjtnC/AOqiI0q9NDBbQXln0uj1YKYtw=='),
                                                                  (
                                                                      'ds:KeyInfo',
                                                                      OrderedDict(
                                                                          [
                                                                              (
                                                                                  'ds:X509Data',
                                                                                  OrderedDict(
                                                                                      [
                                                                                          (
                                                                                              'ds:X509Certificate',
                                                                                              'MIIEAzCCAuugAwIBAgIJAPFNssMgs2XIMA0GCSqGSIb3DQEBCwUAMIGXMQswCQYDVQQGEwJVUzELMAkGA1UECAwCTlkxETAPBgNVBAcMCFB1cmNoYXNlMRkwFwYDVQQKDBBQdXJjaGFzZSBDb2xsZWdlMQwwCgYDVQQLDANDVFMxGjAYBgNVBAMMEXNhbWwucHVyY2hhc2UuZWR1MSMwIQYJKoZIhvcNAQkBFhRzeXN0ZW1zQHB1cmNoYXNlLmVkdTAeFw0xNjAyMjQxNzE0MTFaFw0yNjAyMjMxNzE0MTFaMIGXMQswCQYDVQQGEwJVUzELMAkGA1UECAwCTlkxETAPBgNVBAcMCFB1cmNoYXNlMRkwFwYDVQQKDBBQdXJjaGFzZSBDb2xsZWdlMQwwCgYDVQQLDANDVFMxGjAYBgNVBAMMEXNhbWwucHVyY2hhc2UuZWR1MSMwIQYJKoZIhvcNAQkBFhRzeXN0ZW1zQHB1cmNoYXNlLmVkdTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALgaCkICNx6PkQkFrjg41PHJ6FdMwj5fDOzCLAceX9SGnOUMQXEceQG8I91u0g0zSzbXSajHuuLxY3XN+qQNXPr2MWG8EfP0P3Zdsm5E1Y7d6gwr88j6I6cyxm6Qb4W93PK82oM56wAWbIBmQFSE//9SEDADJfrZudLkCs57ZOfYQvlb9X3U0zv0wdpvhXNilvx8Eke/bi3GlNXl0BNhAROswvq9ZTipvBCDftNdU1N4OOnANDDzEZdRp8eOOJdX261hHSxNojcj7Y0DjBCHxqfxSk2d0tbJzoezE+nvCkLFa2i3NHcIvZVxndGXAC0ROLxU4Y98u5IpdqFovqu4sUUCAwEAAaNQME4wHQYDVR0OBBYEFKW6czrN7ktf2XsWPqaiVbF0YhBtMB8GA1UdIwQYMBaAFKW6czrN7ktf2XsWPqaiVbF0YhBtMAwGA1UdEwQFMAMBAf8wDQYJKoZIhvcNAQELBQADggEBALDm5KpXg4S+qxQQa5LWgezWF5Nl+v+RivZ+/bg/YoWTi+LMQZVoRRqMgTsgpjt1FbIe9/wsJWdk42SHSExISHrSIBG1U2vTtG83HUNwnZWqHu+SxNST+HsZVEtizHH6urqvI8iSxXkvin09srvikQWuMdjp8BwL2REaGEB2bBQQcPlbrILsCSUYKMt4x+5uTi6F3SuY43IAVzIXgonqZf39a8LqjS+Qv0IdSyz2nZfLIfXqPcTXkMPKqEOPt4KP1O6qWQSqZ4p3Ua4fkOwHfHEXJolBToNGQ03SUtXlQhEZqhn/zH7uqhkyIj6xGenz8C7G8zipXSj7RM+Qt3dXA0M=')]))]))])),
                                                             (
                                                                 'saml:Subject',
                                                                 OrderedDict([('saml:NameID', OrderedDict([(
                                                                     '@Format',
                                                                     'urn:oasis:names:tc:SAML:2.0:nameid-format:emailAddress'),
                                                                     (
                                                                         '@SPNameQualifier',
                                                                         'https://nam04.safelinks.protection.outlook.com/?url=https%3A%2F%2Fwww.okta.com%2Fsaml2%2Fservice-provider%2Fspimlojy14FO1GxnP0x7&data=02%7C01%7Cper74005%40adobe.com%7Cde0b15077fb54954505808d72665e2b0%7Cfa7b1b5a7b34438794aed2c178decee1%7C0%7C0%7C637020091353497110&sdata=unNjwnWmXBULTVK%2F8Q%2BEi6NPBgFG%2FIcnAYFJEBusAtY%3D&reserved=0'),
                                                                     (
                                                                         '#text',
                                                                         'user_email@example.com')])),
                                                                              ('saml:SubjectConfirmation',
                                                                               OrderedDict([('@Method',
                                                                                             'urn:oasis:names:tc:SAML:2.0:cm:bearer'),
                                                                                            (
                                                                                                'saml:SubjectConfirmationData',
                                                                                                OrderedDict(
                                                                                                    [(
                                                                                                        '@InResponseTo',
                                                                                                        'id12571430288981441996829275'),
                                                                                                        (
                                                                                                            '@NotOnOrAfter',
                                                                                                            '2019-08-21T18:36:28Z'),
                                                                                                        (
                                                                                                            '@Recipient',
                                                                                                            'https://nam04.safelinks.protection.outlook.com/?url=https%3A%2F%2Fadbe-purchase-d-edu-a37f-prd.okta.com%2Fauth%2Fsaml20%2Faccauthlinktest&data=02%7C01%7Cper74005%40adobe.com%7Cde0b15077fb54954505808d72665e2b0%7Cfa7b1b5a7b34438794aed2c178decee1%7C0%7C0%7C637020091353497110&sdata=UZbER48o6xYKD3EQ7o0NQNuWS9ehOXSkwXsmpPuoLMg%3D&reserved=0')]))]))])),
                                                             ('saml:Conditions', OrderedDict(
                                                                 [('@NotBefore', '2019-08-21T18:30:58Z'),
                                                                  ('@NotOnOrAfter', '2019-08-21T18:36:28Z'), (
                                                                      'saml:AudienceRestriction',
                                                                      OrderedDict([('saml:Audience',
                                                                                    'https://https://adobe-entity-id')]))])),
                                                             ('saml:AuthnStatement', OrderedDict(
                                                                 [('@AuthnInstant', '2019-08-21T18:31:28Z'), (
                                                                     '@SessionIndex',
                                                                     '_a5eecd3b5738a5ea770533f77c18b48cf007d84f1b'),
                                                                  ('@SessionNotOnOrAfter', '2019-08-22T02:31:28Z'), (
                                                                      'saml:AuthnContext', OrderedDict([(
                                                                          'saml:AuthnContextClassRef',
                                                                          'urn:oasis:names:tc:SAML:2.0:ac:classes:Password')]))])),
                                                             ('saml:AttributeStatement',
                                                              OrderedDict([('saml:Attribute', [
                                                                  OrderedDict(
                                                                      [('@Name', 'LastName'), ('saml:AttributeValue',
                                                                                               OrderedDict([(
                                                                                                   '@xsi:type',
                                                                                                   'xs:string'),
                                                                                                   ('#text',
                                                                                                    'user_lastname')]))]),
                                                                  OrderedDict([('@Name', 'FirstName'), (
                                                                      'saml:AttributeValue', OrderedDict(
                                                                          [('@xsi:type', 'xs:string'),
                                                                           ('#text', 'user_firstname')]))]),
                                                                  OrderedDict(
                                                                      [('@Name', 'Email'), ('saml:AttributeValue',
                                                                                            OrderedDict([(
                                                                                                '@xsi:type',
                                                                                                'xs:string'),
                                                                                                ('#text',
                                                                                                 'user_email@example.com')]))]),
                                                                  OrderedDict(
                                                                      [('@Name', 'Other'), ('saml:AttributeValue',
                                                                                            OrderedDict([(
                                                                                                '@xsi:type',
                                                                                                'xs:string'),
                                                                                                ('#text',
                                                                                                 'other attribute')]))])])]))]))]))])


@pytest.fixture
def saml2_file_dict():
    return OrderedDict([('saml2p:Response', OrderedDict(
        [('@Destination', 'https://federatedid-na1.services.adobe.com/federated/saml/SSO'),
         ('@ID', 'id16126125834825116874580727'), ('@IssueInstant', '2019-10-01T21:24:26.284Z'), ('@Version', '2.0'),
         ('@xmlns:saml2p', 'urn:oasis:names:tc:SAML:2.0:protocol'), ('@xmlns:xs', 'http://www.w3.org/2001/XMLSchema'), (
             'saml2:Issuer', OrderedDict([('@Format', 'urn:oasis:names:tc:SAML:2.0:nameid-format:entity'),
                                          ('@xmlns:saml2', 'urn:oasis:names:tc:SAML:2.0:assertion'),
                                          ('#text', 'http://www.okta.com/exkm9aa2veAUERN130x7')])), ('ds:Signature',
                                                                                                     OrderedDict(
                                                                                                         [('@xmlns:ds',
                                                                                                           'http://www.w3.org/2000/09/xmldsig#'),
                                                                                                          (
                                                                                                              'ds:SignedInfo',
                                                                                                              OrderedDict(
                                                                                                                  [(
                                                                                                                      'ds:CanonicalizationMethod',
                                                                                                                      OrderedDict(
                                                                                                                          [
                                                                                                                              (
                                                                                                                                  '@Algorithm',
                                                                                                                                  'http://www.w3.org/2001/10/xml-exc-c14n#')])),
                                                                                                                      (
                                                                                                                          'ds:SignatureMethod',
                                                                                                                          OrderedDict(
                                                                                                                              [
                                                                                                                                  (
                                                                                                                                      '@Algorithm',
                                                                                                                                      'http://www.w3.org/2000/09/xmldsig#rsa-sha1')])),
                                                                                                                      (
                                                                                                                          'ds:Reference',
                                                                                                                          OrderedDict(
                                                                                                                              [
                                                                                                                                  (
                                                                                                                                      '@URI',
                                                                                                                                      '#id16126125834825116874580727'),
                                                                                                                                  (
                                                                                                                                      'ds:Transforms',
                                                                                                                                      OrderedDict(
                                                                                                                                          [
                                                                                                                                              (
                                                                                                                                                  'ds:Transform',
                                                                                                                                                  [
                                                                                                                                                      OrderedDict(
                                                                                                                                                          [
                                                                                                                                                              (
                                                                                                                                                                  '@Algorithm',
                                                                                                                                                                  'http://www.w3.org/2000/09/xmldsig#enveloped-signature')]),
                                                                                                                                                      OrderedDict(
                                                                                                                                                          [
                                                                                                                                                              (
                                                                                                                                                                  '@Algorithm',
                                                                                                                                                                  'http://www.w3.org/2001/10/xml-exc-c14n#'),
                                                                                                                                                              (
                                                                                                                                                                  'ec:InclusiveNamespaces',
                                                                                                                                                                  OrderedDict(
                                                                                                                                                                      [
                                                                                                                                                                          (
                                                                                                                                                                              '@PrefixList',
                                                                                                                                                                              'xs'),
                                                                                                                                                                          (
                                                                                                                                                                              '@xmlns:ec',
                                                                                                                                                                              'http://www.w3.org/2001/10/xml-exc-c14n#')]))])])])),
                                                                                                                                  (
                                                                                                                                      'ds:DigestMethod',
                                                                                                                                      OrderedDict(
                                                                                                                                          [
                                                                                                                                              (
                                                                                                                                                  '@Algorithm',
                                                                                                                                                  'http://www.w3.org/2000/09/xmldsig#sha1')])),
                                                                                                                                  (
                                                                                                                                      'ds:DigestValue',
                                                                                                                                      '4CxbqmMlONSKeScX5jdQy6tpy2E=')]))])),
                                                                                                          (
                                                                                                              'ds:SignatureValue',
                                                                                                              'jj6ZEaUkdGhy4dKAsjSL8Znx2T/SZdqObnvLPPjfLaD5x1lx0KiRCrXUCTMmnFkbh07CC0nLO/bB9Q9lcKbhgtR5+RWgrJq51MZeossBcT5pptsBollxbQ/O9Lwv7sO/NMhxgz0UiIGU1ICasplqK5ctsRFKrRjNqtIS0w25fikWkEFjfuEvleZAiBf9IlPDDiA48QEMpEED2D2Bu22s7mHB0r6ishPbnTAb3IkHX5XgmsHeNqQf8AvZdCepq9jjL8KXZkkD6WpY73zgWKaDS8O59evuUVu4C+//ttIn8Hv5+ubRpJIUIZlmfNOJStEb55oorHFtvuMXyYnaUQ6z5A=='),
                                                                                                          ('ds:KeyInfo',
                                                                                                           OrderedDict([
                                                                                                               (
                                                                                                                   'ds:X509Data',
                                                                                                                   OrderedDict(
                                                                                                                       [
                                                                                                                           (
                                                                                                                               'ds:X509Certificate',
                                                                                                                               'MIIEA..saml2..signing..cert..M=')]))]))])),
         ('saml2p:Status', OrderedDict([('@xmlns:saml2p', 'urn:oasis:names:tc:SAML:2.0:protocol'), (
             'saml2p:StatusCode', OrderedDict([('@Value', 'urn:oasis:names:tc:SAML:2.0:status:Success')]))])), (
             'saml2:Assertion', OrderedDict(
                 [('@ID', 'id161261258348994161047104768'), ('@IssueInstant', '2019-10-01T21:24:26.284Z'),
                  ('@Version', '2.0'),
                  ('@xmlns:saml2', 'urn:oasis:names:tc:SAML:2.0:assertion'),
                  ('@xmlns:xs', 'http://www.w3.org/2001/XMLSchema'),
                  ('saml2:Issuer', OrderedDict([('@Format', 'urn:oasis:names:tc:SAML:2.0:nameid-format:entity'),
                                                ('@xmlns:saml2', 'urn:oasis:names:tc:SAML:2.0:assertion'),
                                                ('#text', 'http://www.okta.com/exkm9aa2veAUERN130x7')])),
                  ('ds:Signature',
                   OrderedDict([(
                       '@xmlns:ds',
                       'http://www.w3.org/2000/09/xmldsig#'),
                       (
                           'ds:SignedInfo',
                           OrderedDict(
                               [(
                                   'ds:CanonicalizationMethod',
                                   OrderedDict(
                                       [
                                           (
                                               '@Algorithm',
                                               'http://www.w3.org/2001/10/xml-exc-c14n#')])),
                                   (
                                       'ds:SignatureMethod',
                                       OrderedDict(
                                           [
                                               (
                                                   '@Algorithm',
                                                   'http://www.w3.org/2000/09/xmldsig#rsa-sha1')])),
                                   (
                                       'ds:Reference',
                                       OrderedDict(
                                           [
                                               (
                                                   '@URI',
                                                   '#id161261258348994161047104768'),
                                               (
                                                   'ds:Transforms',
                                                   OrderedDict(
                                                       [
                                                           (
                                                               'ds:Transform',
                                                               [
                                                                   OrderedDict(
                                                                       [
                                                                           (
                                                                               '@Algorithm',
                                                                               'http://www.w3.org/2000/09/xmldsig#enveloped-signature')]),
                                                                   OrderedDict(
                                                                       [
                                                                           (
                                                                               '@Algorithm',
                                                                               'http://www.w3.org/2001/10/xml-exc-c14n#'),
                                                                           (
                                                                               'ec:InclusiveNamespaces',
                                                                               OrderedDict(
                                                                                   [
                                                                                       (
                                                                                           '@PrefixList',
                                                                                           'xs'),
                                                                                       (
                                                                                           '@xmlns:ec',
                                                                                           'http://www.w3.org/2001/10/xml-exc-c14n#')]))])])])),
                                               (
                                                   'ds:DigestMethod',
                                                   OrderedDict(
                                                       [
                                                           (
                                                               '@Algorithm',
                                                               'http://www.w3.org/2000/09/xmldsig#sha1')])),
                                               (
                                                   'ds:DigestValue',
                                                   'cehkiOw3Z4fJHfljLMC2vEt6dzA=')]))])),
                       (
                           'ds:SignatureValue',
                           'ibakJk5OjtlMqTNmdtd0RdOge9StxFIz+ccnSvOouGtAYCCPhAcOSTPIkvrecRpQxMiUXyyUbQ2gCySFoeRH67ZjieZ+V+30bLofwBnHaXWXXRq2IJ72kMFQC8ugJb8OmJuvfjjJ6FgzUjSTXFD5k4gx0YZNSVQk+jD3ZoByaD80qRXqDJBTbGSQDVnD7IXo0MJBlbBbG1dB2GjNNk84m3q3UkQ7rMYduvRGhy0FKOPicuitKq73/feJJi2UyPpblktmCHa+NmfwtVMS/LbfKIyGtgId9hNKBnWcT2rO5hjKTPcLZPNVs+la6n+uLE5R6jtr6b6WJDorgffJtWSTkw=='),
                       (
                           'ds:KeyInfo',
                           OrderedDict(
                               [(
                                   'ds:X509Data',
                                   OrderedDict(
                                       [
                                           (
                                               'ds:X509Certificate',
                                               'MIID3DCCAsSgAwIBAgIGAWq3tSNMMA0GCSqGSIb3DQEBCwUAMIGuMQswCQYDVQQGEwJVUzETMBEG\n                        A1UECAwKQ2FsaWZvcm5pYTEWMBQGA1UEBwwNU2FuIEZyYW5jaXNjbzENMAsGA1UECgwET2t0YTEU\n                        MBIGA1UECwwLU1NPUHJvdmlkZXIxLzAtBgNVBAMMJmFkYmUtNGNkNzY3NWQ1Y2RiMGJiMDBhNDk1\n                        Y2JlLTRkZWUtcHJkMRwwGgYJKoZIhvcNAQkBFg1pbmZvQG9rdGEuY29tMB4XDTE5MDUxNDE4NTY0\n                        MloXDTI5MDUxNDE4NTc0Mlowga4xCzAJBgNVBAYTAlVTMRMwEQYDVQQIDApDYWxpZm9ybmlhMRYw\n                        FAYDVQQHDA1TYW4gRnJhbmNpc2NvMQ0wCwYDVQQKDARPa3RhMRQwEgYDVQQLDAtTU09Qcm92aWRl\n                        cjEvMC0GA1UEAwwmYWRiZS00Y2Q3Njc1ZDVjZGIwYmIwMGE0OTVjYmUtNGRlZS1wcmQxHDAaBgkq\n                        hkiG9w0BCQEWDWluZm9Ab2t0YS5jb20wggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCQ\n                        ZtZWekQhqPf9nzT8rzCaCy8YRTh9l95rZ0/6rKrfScf9SLjZmjhslRsLcIiN2MjtVxcTv2gPGPIJ\n                        qwQeWF4Il0n0kSPBzdgNscHN9SGkl0ayAHLOJ8z0upH8I/H6RA5EhONsWkKXM7ZK8V5sTnF1Zmag\n                        82Ie9SGfgdpY2AQAhmevCkfwu5fj+asW8FZIrs/FSBxrBfOpdnN7TogI7PQwmMkD9wjIEHKSuD3x\n                        +fDIv77nYOuOk6tuI1Em9tTF58R8L1wRZkddBWf3n2zgrWJFVAS+bnUAQOX5N88jpS/Wv91AK3pm\n                        7u0nB+ctaBEgabxadDIS6+10NW8sRh/l8n51AgMBAAEwDQYJKoZIhvcNAQELBQADggEBAFZk18oO\n                        FK6KICuKcGIt+KK5APQAn/GwV9eMIw+1naNBDmblCRbsPk0r+HXfbimaMnrgw/ENwN6mZ06SgcVU\n                        rUEJGl3nLVTeoe9JWEfsNEq/3touZ7hx7llKwtO/Bq369j8BNjU1P1F+rDE/8fkjV/T0AArCCPU/\n                        Tpko1z9FL/iS//8xzQWsZkkbOQu+MY5n67m7/l39r0OO7wHvm8jL8izq3FOX3lIIZk0VnfJEh/Eg\n                        45iWbPGdaoBmh1e+xPupXnWj0+m4nBvEHlrAlt7rWoRou2VRDfvPmITPkk54cxYM+GsnzHsOuL+w\n                        lHI28PWX+YVpcZCjZ7eNEwCf+cuS9HU=')]))]))])),
                  ('saml2:Subject',
                   OrderedDict([('@xmlns:saml2', 'urn:oasis:names:tc:SAML:2.0:assertion'), ('saml2:NameID',
                                                                                            OrderedDict([(
                                                                                                '@Format',
                                                                                                'urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified'),
                                                                                                (
                                                                                                    '#text',
                                                                                                    'user_email@example.com')])),
                                ('saml2:SubjectConfirmation', OrderedDict(
                                    [('@Method', 'urn:oasis:names:tc:SAML:2.0:cm:bearer'), (
                                        'saml2:SubjectConfirmationData', OrderedDict(
                                            [('@NotOnOrAfter', '2019-10-01T21:29:26.284Z'), ('@Recipient',
                                                                                             'https://federatedid-na1.services.adobe.com/federated/saml/SSO')]))]))])),
                  ('saml2:Conditions', OrderedDict(
                      [('@NotBefore', '2019-10-01T21:19:26.284Z'), ('@NotOnOrAfter', '2019-10-01T21:29:26.284Z'),
                       ('@xmlns:saml2', 'urn:oasis:names:tc:SAML:2.0:assertion'),
                       ('saml2:AudienceRestriction', OrderedDict(
                           [('saml2:Audience',
                             'https://federatedid-na1.services.adobe.com/federated/saml/metadata')]))])), (
                      'saml2:AuthnStatement', OrderedDict(
                          [('@AuthnInstant', '2019-10-01T21:24:26.284Z'),
                           ('@SessionIndex', 'id1569965066284.1529247874'),
                           ('@xmlns:saml2', 'urn:oasis:names:tc:SAML:2.0:assertion'),
                           ('saml2:AuthnContext', OrderedDict([(
                               'saml2:AuthnContextClassRef',
                               'urn:oasis:names:tc:SAML:2.0:ac:classes:PasswordProtectedTransport')]))])),
                  ('saml2:AttributeStatement', OrderedDict([('@xmlns:saml2', 'urn:oasis:names:tc:SAML:2.0:assertion'), (
                      'saml2:Attribute', [OrderedDict(
                          [('@Name', 'FirstName'),
                           ('@NameFormat', 'urn:oasis:names:tc:SAML:2.0:attrname-format:unspecified'), (
                               'saml2:AttributeValue', OrderedDict([('@xmlns:xs', 'http://www.w3.org/2001/XMLSchema'),
                                                                    ('@xmlns:xsi',
                                                                     'http://www.w3.org/2001/XMLSchema-instance'),
                                                                    ('@xsi:type', 'xs:string'),
                                                                    ('#text', 'user_firstname')]))]),
                          OrderedDict(
                              [('@Name', 'LastName'),
                               ('@NameFormat', 'urn:oasis:names:tc:SAML:2.0:attrname-format:unspecified'), (
                                   'saml2:AttributeValue',
                                   OrderedDict([('@xmlns:xs', 'http://www.w3.org/2001/XMLSchema'),
                                                ('@xmlns:xsi',
                                                 'http://www.w3.org/2001/XMLSchema-instance'),
                                                ('@xsi:type', 'xs:string'), ('#text', 'user_lastname')]))]),
                          OrderedDict(
                              [('@Name', 'Email'),
                               ('@NameFormat', 'urn:oasis:names:tc:SAML:2.0:attrname-format:unspecified'), (
                                   'saml2:AttributeValue',
                                   OrderedDict([('@xmlns:xs', 'http://www.w3.org/2001/XMLSchema'),
                                                ('@xmlns:xsi',
                                                 'http://www.w3.org/2001/XMLSchema-instance'),
                                                ('@xsi:type', 'xs:string'),
                                                ('#text', 'user_email@example.com')]))])])]))]))]))])
