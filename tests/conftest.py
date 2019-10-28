import pytest


@pytest.fixture
def descriptions():
    return {'metadata': {'issuer_url': 'Must match Entity ID attribute value from Adobe Metadata',
                         'destination': 'Must match Location attribute value from Adobe Metadata',
                         'signature_method_algorithm': 'Should be rsa-sha1',
                         'digest_method_algorithm': 'Should be rsa-sha1',
                         'assertion_attributes': 'Attributes included in your SAML assertion',
                         'name_id_format': 'Format of your Name-ID attribute',
                         'name_id': 'Name-ID attribute, format of attribute must match your login setting of your federated directory',
                         'signing_cert': 'Token-Signing Certificate, must be Base-64 encoded X.509(.CER), which is equivalent to a PEM format certificate',
                         'time_sent': "Timestamp must be within the 'not_before' and 'not_on_or_after' time window"},
            'error_message': {'no_attributes': 'Assertion attributes not released',
                              'signature_method_algorithm': 'Should be rsa-sha1',
                              'digest_method_algorithm': 'Should be rsa-sha1',
                              'assertion_attributes': 'Assertion must include FirstName, LastName, and Email',
                              'name_id_format': 'Name-ID requires unspecified or emailAddress format',
                              'name_id': 'Name-ID attribute must be present with unspecified or emailAddress format',
                              'signing_cert': 'Signing cert not present',
                              'time_sent': "Timestamp must be within the 'not_before' and 'not_on_or_after' time window"}}


@pytest.fixture
def idp_repo():
    return {'adfs': {'name': 'adfs',
                     'helpx': 'https://helpx.adobe.com/enterprise/kb/configure-microsoft-ad-fs-with-sso.html',
                     'error_codes': {
                         'assertion_attributes': {'hint': 'Review Steps 8 - 14', 'link': '#ConfiguretheADFSserver'},
                         'name_id': {'hint': 'Please review step 11', 'link': '#ConfiguretheADFSserver'},
                         'name_id_format': {'hint': 'Please review step 11', 'link': '#ConfiguretheADFSserver'},
                         'issuer_url': {'hint': 'Please review step 2', 'link': '#ConfiguretheADFSserver'},
                         'destination': {'hint': 'Please review step 2', 'link': '#ConfiguretheADFSserver'},
                         'signature_method': {'hint': 'Please review step 16', 'link': '#ConfiguretheADFSserver'},
                         'digest_method': {'hint': 'Please review step 16',
                                           'link': '#ConfiguretheADFSserver'}}},
            'shibboleth': {'name': 'shibboleth',
                           'helpx': 'https://helpx.adobe.com/enterprise/kb/configure-shibboleth-with-adobe-sso.html',
                           'error_codes': {
                               'assertion_attributes': {
                                   'hint': 'please review step 2 link 1 and step 1 from link2',
                                   'link': [
                                       '#ConfigureShibboleth',
                                       '#TroubleshootyourShibbolethsetup']},
                               'name_id': {
                                   'hint': 'Please review step 11',
                                   'link': '#TroubleshootyourShibbolethsetup'},
                               'name_id_format': {
                                   'hint': 'please review step 2 from link 1 and step 8 from link2',
                                   'link': [
                                       '#ConfigureShibboleth',
                                       '#TroubleshootyourShibbolethsetup']},
                               'issuer_url': {
                                   'hint': 'Please review step 3',
                                   'link': '#ConfigureShibboleth'},
                               'destination': {
                                   'hint': 'Please review step 3',
                                   'link': '#ConfigureShibboleth'}}}

        , 'azure': {'name': 'azure',
                    'helpx': 'https://helpx.adobe.com/enterprise/kb/configure-shibboleth-with-adobe-sso.html',
                    'error_codes': {
                        'assertion_attributes': {'hint': 'Review Steps 8 - 14', 'link': '#ConfiguretheADFSserver'},
                        'name_id': {'hint': 'Please review step 11', 'link': '#ConfiguretheADFSserver'},
                        'name_id_format': {'hint': None, 'link': None}, 'issuer_url': {'hint': None, 'link': None},
                        'destination': {'hint': None, 'link': None}, 'signature_method': {'hint': None, 'link': None},
                        'digest_method': {'hint': None, 'link': None}}}}
