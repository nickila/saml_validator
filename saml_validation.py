from idp import IDP

from testing_trace_labels import saml
from testing_trace_labels import saml2

def saml_analysis(dict_saml_trace):
    list_errors = []
    saml_trace_values = {}
    key = 'saml2' if '2' in list(dict_saml_trace.keys())[0] else 'saml'
    try:
        attribute_assertions = {}
        for each in dict_saml_trace[key + 'p:Response'][key + ':Assertion'][key + ':AttributeStatement'][key + ':Attribute']:
            attribute_assertions[each['@Name']] = each[key + ':AttributeValue']['#text']

        saml_trace_values['assertion_attributes'] = attribute_assertions
    except:
        saml_trace_values['attributes_released'] = "None or empty values present"
        list_errors.append('Empty or non present attributes')

    saml_trace_values['name_id'] = dict_saml_trace[key + 'p:Response'][key + ':Assertion'][key + ':Subject'][key + ':NameID']['#text']
    saml_trace_values['name_id_format'] = dict_saml_trace[key + 'p:Response'][key + ':Assertion'][key + ':Subject'][key + ':NameID']['@Format']

    #ACS Url aka Reply URL, Location value from adobe metadata
    saml_trace_values['destination'] = dict_saml_trace[key + 'p:Response']['@Destination']

    # Issuer URL, Entity ID from adobe metadata
    saml_trace_values['issuer_url'] = dict_saml_trace[key + 'p:Response'][key + ':Assertion'][key + ':Conditions'][key + ':AudienceRestriction'][key + ':Audience']

    saml_trace_values['signature_method_algorithm'] = dict_saml_trace[key + 'p:Response']['ds:Signature']['ds:SignedInfo']['ds:SignatureMethod']['@Algorithm']
    saml_trace_values['digest_method_algorithm'] = dict_saml_trace[key + 'p:Response']['ds:Signature']['ds:SignedInfo']['ds:Reference']['ds:DigestMethod']['@Algorithm']

    saml_trace_values['not_before'] = dict_saml_trace[key + 'p:Response'][key + ':Assertion'][key + ':Conditions']['@NotBefore']
    saml_trace_values['time_sent'] = dict_saml_trace[key + 'p:Response']['@IssueInstant']
    saml_trace_values['not_on_or_after'] = dict_saml_trace[key + 'p:Response'][key + ':Assertion'][key + ':Conditions']['@NotOnOrAfter']

    try:
        saml_trace_values['signing_cert'] = dict_saml_trace[key + 'p:Response']['ds:Signature']['ds:KeyInfo']['ds:X509Data']['ds:X509Certificate']
    except:
        list_errors.append('Check presence and/or format of signing cert')

    return saml_trace_values, list_errors

saml_analysis(saml, saml2)
