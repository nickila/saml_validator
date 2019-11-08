import pytest


@pytest.fixture
def saml_parsed_dict():
    return {'assertion_attributes': {'LastName': 'example_last_name', 'FirstName': 'example_first_name',
                                     'Email': 'email@example.edu', 'Other': 'other attribute'},
            'name_id': '22334384CCCCE66c123', 'name_id_format': 'urn:oasis:names:tc:SAML:2.0:nameid-format:emailAddress',
            'destination': 'https://https://adobe-location-from_meta', 'issuer_url': 'https://https://adobe-entity-id',
            'signature_method_algorithm': 'https://www.w3.org/2000/09/xmldsig#rsa-sha1',
            'digest_method_algorithm': 'https://www.w3.org/2000/09/xmldsig#rsa-sha1',
            'not_before': '2019-08-21T18:30:58Z', 'time_sent': '2019-08-21T18:36:29Z',
            'not_on_or_after': '2019-08-21T18:36:28Z',
            'signing_cert': 'MIIEA_signing_cert_saml',
            'in_response_to': 'id18283838494959494949'}


@pytest.fixture
def saml2_parsed_dict():
    return {'assertion_attributes': {'LastName': 'example_last_name', 'FirstName': 'example_first_name',
                                     'Email': 'email@example.edu', 'Other': 'other attribute'},
            'name_id': '22334384CCCCE66c123', 'name_id_format': 'urn:oasis:names:tc:SAML:2.0:nameid-format:emailAddress',
            'destination': 'https://https://adobe-location-from_meta', 'issuer_url': 'https://https://adobe-entity-id',
            'signature_method_algorithm': 'https://www.w3.org/2000/09/xmldsig#rsa-sha1',
            'digest_method_algorithm': 'https://www.w3.org/2000/09/xmldsig#rsa-sha1',
            'not_before': '2019-08-21T18:30:58Z', 'time_sent': '2019-08-21T18:36:29Z',
            'not_on_or_after': '2019-08-21T18:36:28Z',
            'signing_cert': 'MIIEA_signing_cert_saml2',
            'in_response_to': 'id18283838494959494949'}


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
    return {'adfs': {'helpx': 'https://helpx.adobe.com/enterprise/kb/configure-microsoft-ad-fs-with-sso.html',
                     'error_codes': {'assertion_attributes': {'hint': 'Review Steps 8 - 14', 'links': [
                         'https://helpx.adobe.com/enterprise/kb/configure-microsoft-ad-fs-with-sso.html#ConfiguretheADFSserver']},
                                     'name_id': {'hint': 'Please review step 11', 'links': [
                                         'https://helpx.adobe.com/enterprise/kb/configure-microsoft-ad-fs-with-sso.html#ConfiguretheADFSserver']},
                                     'name_id_format': {'hint': 'Please review step 11', 'links': [
                                         'https://helpx.adobe.com/enterprise/kb/configure-microsoft-ad-fs-with-sso.html#ConfiguretheADFSserver']},
                                     'issuer_url': {'hint': 'Please review step 2', 'links': [
                                         'https://helpx.adobe.com/enterprise/kb/configure-microsoft-ad-fs-with-sso.html#ConfiguretheADFSserver']},
                                     'destination': {'hint': 'Please review step 2', 'links': [
                                         'https://helpx.adobe.com/enterprise/kb/configure-microsoft-ad-fs-with-sso.html#ConfiguretheADFSserver']},
                                     'signature_method': {'hint': 'Please review step 16', 'links': [
                                         'https://helpx.adobe.com/enterprise/kb/configure-microsoft-ad-fs-with-sso.html#ConfiguretheADFSserver']},
                                     'digest_method': {'hint': 'Please review step 16', 'links': [
                                         'https://helpx.adobe.com/enterprise/kb/configure-microsoft-ad-fs-with-sso.html#ConfiguretheADFSserver']}}},
            'shibboleth': {'helpx': 'https://helpx.adobe.com/enterprise/kb/configure-shibboleth-with-adobe-sso.html',
                           'error_codes': {'assertion_attributes': {
                               'hint': 'please review step 2 from links 1 and step 1 from links2', 'links': [
                                   'https://helpx.adobe.com/enterprise/kb/configure-shibboleth-with-adobe-sso.html#ConfigureShibboleth',
                                   'https://helpx.adobe.com/enterprise/kb/configure-shibboleth-with-adobe-sso.html#TroubleshootyourShibbolethsetup']},
                               'name_id': {'hint': 'Please review step 11',
                                           'links': ['#TroubleshootyourShibbolethsetup']},
                               'name_id_format': {
                                   'hint': 'please review step 2 from links 1 and step 8 from links2',
                                   'links': [
                                       'https://helpx.adobe.com/enterprise/kb/configure-shibboleth-with-adobe-sso.html#ConfigureShibboleth',
                                       'https://helpx.adobe.com/enterprise/kb/configure-shibboleth-with-adobe-sso.html#TroubleshootyourShibbolethsetup']},
                               'issuer_url': {'hint': 'Please review step 3', 'links': [
                                   'https://helpx.adobe.com/enterprise/kb/configure-shibboleth-with-adobe-sso.html#ConfigureShibboleth']},
                               'destination': {'hint': 'Please review step 3', 'links': [
                                   'https://helpx.adobe.com/enterprise/kb/configure-shibboleth-with-adobe-sso.html#ConfigureShibboleth']}}},
            'azure': {'helpx': 'https://helpx.adobe.com/enterprise/kb/configure-microsoft-azure-with-adobe-sso.html',
                      'error_codes': {'assertion_attributes': {'hint': 'Review Steps 8 - 9', 'links': [
                          'https://helpx.adobe.com/enterprise/kb/configure-microsoft-azure-with-adobe-sso.html#CreatingSSOApplicationinAzureforAdobe']},
                                      'name_id': {'hint': 'Review Step 9 "note"', 'links': [
                                          'https://helpx.adobe.com/enterprise/kb/configure-microsoft-azure-with-adobe-sso.html#CreatingSSOApplicationinAzureforAdobe']},
                                      'name_id_format': {'hint': 'Review Step 9 "note"', 'links': [
                                          'https://helpx.adobe.com/enterprise/kb/configure-microsoft-azure-with-adobe-sso.html#CreatingSSOApplicationinAzureforAdobe']},
                                      'issuer_url': {'hint': 'Review Steps 7, 20, 21', 'links': [
                                          'https://helpx.adobe.com/enterprise/kb/configure-microsoft-azure-with-adobe-sso.html#CreatingSSOApplicationinAzureforAdobe']},
                                      'destination': {'hint': 'Review Steps 7, 20, 21', 'links': [
                                          'https://helpx.adobe.com/enterprise/kb/configure-microsoft-azure-with-adobe-sso.html#CreatingSSOApplicationinAzureforAdobe']},
                                      'signing_cert': {'hint': 'Review Steps 10, 15, 16', 'links': [
                                          'https://helpx.adobe.com/enterprise/kb/configure-microsoft-azure-with-adobe-sso.html#CreatingSSOApplicationinAzureforAdobe']}}},
            'okta': {'helpx': 'https://helpx.adobe.com/enterprise/kb/configure-okta-with-adobe-sso.html',
                     'error_codes': {'assertion_attributes': {'hint': 'Review Step 2', 'links': [
                         'https://helpx.adobe.com/enterprise/kb/configure-okta-with-adobe-sso.html#ConfigureOkta']},
                                     'name_id': {'hint': 'Review Step 2', 'links': [
                                         'https://helpx.adobe.com/enterprise/kb/configure-okta-with-adobe-sso.html#ConfigureOkta']},
                                     'issuer_url': {'hint': 'Review Step 4 from links1 and Steps 4, 5 from links2',
                                                    'links': [
                                                        'https://helpx.adobe.com/enterprise/kb/configure-okta-with-adobe-sso.html#DownloadthesecuritycertificatefromOkta',
                                                        'https://helpx.adobe.com/enterprise/kb/configure-okta-with-adobe-sso.html#ConfigureOkta']},
                                     'destination': {'hint': 'Review Step 4 from links1 and Steps 4, 5 from links2',
                                                     'links': [
                                                         'https://helpx.adobe.com/enterprise/kb/configure-okta-with-adobe-sso.html#DownloadthesecuritycertificatefromOkta',
                                                         'https://helpx.adobe.com/enterprise/kb/configure-okta-with-adobe-sso.html#ConfigureOkta']},
                                     'signing_cert': {'hint': 'Review Step 1-4', 'links': [
                                         'https://helpx.adobe.com/enterprise/kb/configure-okta-with-adobe-sso.html#DownloadthesecuritycertificatefromOkta']}}},
            'google': {'helpx': 'https://helpx.adobe.com/enterprise/kb/configure-google-with-adobe-sso.html',
                       'error_codes': {'assertion_attributes': {'hint': 'Review Steps 2 - 3', 'links': [
                           'https://helpx.adobe.com/enterprise/kb/configure-google-with-adobe-sso.html#ConfiguretheGoogleAdminConsole']},
                                       'name_id': {'hint': 'Review Step 1', 'links': [
                                           'https://helpx.adobe.com/enterprise/kb/configure-google-with-adobe-sso.html#ConfiguretheGoogleAdminConsole']},
                                       'name_id_format': {'hint': 'Review Step 1', 'links': [
                                           'https://helpx.adobe.com/enterprise/kb/configure-google-with-adobe-sso.html#ConfiguretheGoogleAdminConsole']},
                                       'issuer_url': {'hint': 'Review Step 4 from links1 and Step 1 from links 2',
                                                      'links': [
                                                          'https://helpx.adobe.com/enterprise/kb/configure-google-with-adobe-sso.html#ConfigureAdobeAdminConsole',
                                                          'https://helpx.adobe.com/enterprise/kb/configure-google-with-adobe-sso.html#ConfiguretheGoogleAdminConsole']},
                                       'destination': {'hint': 'Review Step 4 from links1 and Step 1 from links 2 ',
                                                       'links': [
                                                           'https://helpx.adobe.com/enterprise/kb/configure-google-with-adobe-sso.html#ConfigureAdobeAdminConsole',
                                                           'https://helpx.adobe.com/enterprise/kb/configure-google-with-adobe-sso.html#ConfiguretheGoogleAdminConsole']},
                                       'signing_cert': {'hint': 'Review step 2', 'links': [
                                           'https://helpx.adobe.com/enterprise/kb/configure-google-with-adobe-sso.html#SetupGoogleAdminConsole']}}},
            'wso2': {'helpx': 'https://helpx.adobe.com/enterprise/kb/configure-wso2-idp-adobe-sso.html',
                     'error_codes': {'assertion_attributes': {'hint': 'Review Step 6, and 10.5', 'links': [
                         'https://helpx.adobe.com/enterprise/kb/configure-wso2-idp-adobe-sso.html#Registernewserviceprovider']},
                                     'name_id': {'hint': 'Please review step 6', 'links': [
                                         'https://helpx.adobe.com/enterprise/kb/configure-wso2-idp-adobe-sso.html#Registernewserviceprovider']},
                                     'name_id_format': {'hint': 'Please review step 6 and 10.3', 'links': [
                                         'https://helpx.adobe.com/enterprise/kb/configure-wso2-idp-adobe-sso.html#Registernewserviceprovider']},
                                     'issuer_url': {'hint': 'Please review step 7, 10.1', 'links': [
                                         'https://helpx.adobe.com/enterprise/kb/configure-wso2-idp-adobe-sso.html#Registernewserviceprovider']},
                                     'destination': {'hint': 'Please review step 7, 10.2', 'links': [
                                         'https://helpx.adobe.com/enterprise/kb/configure-wso2-idp-adobe-sso.html#Registernewserviceprovider']}}}}
