from backend_app.saml_result import SamlResult


class Analyzer:
    @classmethod
    def process(cls, saml_dict, descriptions, idp_info=None):
        saml_values = cls.parse_saml(saml_dict)
        return cls.analyze(saml_values, descriptions, idp_info)

    @classmethod
    def parse_saml(cls, dict_saml_trace):
        saml_trace_values = {}
        key = 'saml2' if '2' in list(dict_saml_trace.keys())[0] else 'saml'
        attributes_released = []
        try:
            attributes_released = dict_saml_trace[key + 'p:Response'][key + ':Assertion'][key + ':AttributeStatement'][
                key + ':Attribute']
        except:
            saml_trace_values['assertion_attributes'] = None
        if len(attributes_released) != 0:
            assertion_attributes = {}
            for each in attributes_released:
                try:
                    assertion_attributes[each['@Name']] = each[key + ':AttributeValue']['#text']
                except:
                    assertion_attributes[each['@Name']] = None
            saml_trace_values['assertion_attributes'] = assertion_attributes
        try:
            saml_trace_values['name_id'] = \
                dict_saml_trace[key + 'p:Response'][key + ':Assertion'][key + ':Subject'][key + ':NameID']['#text']
        except:
            saml_trace_values['name_id'] = None
        try:
            saml_trace_values['name_id_format'] = \
                dict_saml_trace[key + 'p:Response'][key + ':Assertion'][key + ':Subject'][key + ':NameID']['@Format']
        except:
            saml_trace_values['name_id_format'] = None
        saml_trace_values['destination'] = dict_saml_trace[key + 'p:Response']['@Destination']
        saml_trace_values['issuer_url'] = \
            dict_saml_trace[key + 'p:Response'][key + ':Assertion'][key + ':Conditions'][key + ':AudienceRestriction'][
                key + ':Audience']
        saml_trace_values['signature_method_algorithm'] = \
            dict_saml_trace[key + 'p:Response']['ds:Signature']['ds:SignedInfo']['ds:SignatureMethod']['@Algorithm']
        saml_trace_values['digest_method_algorithm'] = \
            dict_saml_trace[key + 'p:Response']['ds:Signature']['ds:SignedInfo']['ds:Reference']['ds:DigestMethod'][
                '@Algorithm']
        saml_trace_values['not_before'] = dict_saml_trace[key + 'p:Response'][key + ':Assertion'][key + ':Conditions'][
            '@NotBefore']
        saml_trace_values['time_sent'] = dict_saml_trace[key + 'p:Response']['@IssueInstant']
        saml_trace_values['not_on_or_after'] = \
            dict_saml_trace[key + 'p:Response'][key + ':Assertion'][key + ':Conditions'][
                '@NotOnOrAfter']
        try:
            saml_trace_values['signing_cert'] = \
                dict_saml_trace[key + 'p:Response']['ds:Signature']['ds:KeyInfo']['ds:X509Data'][
                    'ds:X509Certificate'] if True else None
        except:
            saml_trace_values['signing_cert'] = None
        return saml_trace_values

    @classmethod
    def analyze(cls, saml_values, descriptions, idp_info=None):
        errors = {}
        if not saml_values['assertion_attributes']:
            errors['assertion_attributes'] = {'description': descriptions['error_message']['no_attributes']}
            if idp_info:
                errors['assertion_attributes'].update(idp_info['error_codes']['assertion_attributes'])
        else:
            if not {'FirstName', 'LastName', 'Email'}.issubset(saml_values['assertion_attributes']):
                errors['assertion_attributes'] = {
                    'description': descriptions['error_message']['assertion_attributes']}
                if idp_info:
                    errors['assertion_attributes'].update(idp_info['error_codes']['assertion_attributes'])
            
        if not saml_values['name_id']:
            errors['name_id'][
                'description'] = {'descriptions': descriptions['error_message']['name_id']}
            if idp_info:
                errors['name_id'].update(idp_info['error_codes']['name_id'])

        if not any(item in saml_values['name_id_format'] for item in ['unspecified', 'emailAddress']):
            errors['name_id_format'] = {'description': descriptions['error_message']['name_id_format']}
            if idp_info:
                errors['name_id_format'].update(idp_info['error_codes']['name_id_format'])

        if not saml_values['signing_cert']:
            errors['signing_cert'] = {'description': descriptions['error_message']['signing_cert']}
            if idp_info:
                errors['signing_cert'].update(idp_info['error_codes']['signing_cert'])
            
        return SamlResult.construct_result(saml_values, descriptions, errors)
