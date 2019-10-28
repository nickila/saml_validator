from backend_app.saml_result import SamlResult
from backend_app.error_handler import SamlParsingError


class Analyzer:
    @classmethod
    def process(cls, saml_dict, descriptions, idp_info=None):
        saml_values = cls.parse_saml(saml_dict)
        errors = cls.create_error_dict(saml_values, descriptions.get('error_message'), idp_info)
        return SamlResult.construct_result(saml_values, descriptions.get('metadata'), errors)

    @classmethod
    def parse_saml(cls, dict_saml_trace):
        """
        desciption: This method extracts the saml attributes we are targeting for analysis
        :type dict_saml_trace: dict(result of xmltodict.parse(uploaded XML file))
        :rtype: saml_trace_values: dict(extracted saml values)
        """
        saml_trace_values = {}
        try:
            key = 'saml2' if '2' in list(dict_saml_trace.keys())[0] else 'saml'
        except Exception as e:
            raise SamlParsingError(str(e))
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
        try:
            saml_trace_values['destination'] = dict_saml_trace[key + 'p:Response']['@Destination']
        except:
            saml_trace_values['destination'] = None
        try:
            saml_trace_values['issuer_url'] = \
                dict_saml_trace[key + 'p:Response'][key + ':Assertion'][key + ':Conditions'][
                    key + ':AudienceRestriction'][
                    key + ':Audience']
        except:
            saml_trace_values['issuer_url'] = None
        try:
            saml_trace_values['signature_method_algorithm'] = \
                dict_saml_trace[key + 'p:Response']['ds:Signature']['ds:SignedInfo']['ds:SignatureMethod']['@Algorithm']
        except:
            saml_trace_values['signature_method_algorithm'] = None
        try:
            saml_trace_values['digest_method_algorithm'] = \
                dict_saml_trace[key + 'p:Response']['ds:Signature']['ds:SignedInfo']['ds:Reference']['ds:DigestMethod'][
                    '@Algorithm']
        except:
            saml_trace_values['digest_method_algorithm'] = None

        try:
            saml_trace_values['not_before'] = \
            dict_saml_trace[key + 'p:Response'][key + ':Assertion'][key + ':Conditions'][
                '@NotBefore']
        except:
            saml_trace_values['not_before'] = None
        try:
            saml_trace_values['time_sent'] = dict_saml_trace[key + 'p:Response']['@IssueInstant']
        except:
            saml_trace_values['time_sent'] = None
        try:
            saml_trace_values['not_on_or_after'] = \
                dict_saml_trace[key + 'p:Response'][key + ':Assertion'][key + ':Conditions'][
                    '@NotOnOrAfter']
        except:
            saml_trace_values['not_on_or_after'] = None
        try:
            saml_trace_values['signing_cert'] = \
                dict_saml_trace[key + 'p:Response']['ds:Signature']['ds:KeyInfo']['ds:X509Data'][
                    'ds:X509Certificate'] if True else None
        except:
            saml_trace_values['signing_cert'] = None

        if all(value is None for value in saml_trace_values.values()):
            raise SamlParsingError()

        return saml_trace_values

    @classmethod
    def create_error_dict(cls, saml_values, descriptions, idp_info=None):
        """
        description: Compares saml values with the common errors below
        :type saml_values: dict(parsed saml values from xml upload)
        :type descriptions: dict(metadata from resources/descriptions.yml)
        :type idp_info: dict(session specific idp info from resources/idp.yml )
        :rtype: errors dict(saml errors found)
        """
        errors = {}
        if not saml_values['assertion_attributes']:
            errors['assertion_attributes'] = {'description': descriptions['no_attributes']}
            if idp_info.get('assertion_attributes'):
                errors['assertion_attributes'].update(idp_info['error_codes']['assertion_attributes'])
        else:
            if not {'FirstName', 'LastName', 'Email'}.issubset(saml_values['assertion_attributes']):
                errors['assertion_attributes'] = {
                    'description': descriptions['assertion_attributes']}
                if idp_info.get('assertion_attributes'):
                    errors['assertion_attributes'].update(idp_info['error_codes']['assertion_attributes'])

        if not saml_values['name_id']:
            errors['name_id'] = {'descriptions': descriptions['name_id']}
            if idp_info.get('name_id'):
                errors['name_id'].update(idp_info['error_codes']['name_id'])

        if not saml_values['name_id_format'] or not any(
                item in saml_values['name_id_format'] for item in ['unspecified', 'emailAddress']):
            errors['name_id_format'] = {'description': descriptions['name_id_format']}
            if idp_info.get('name_id_format'):
                errors['name_id_format'].update(idp_info['error_codes']['name_id_format'])

        if not saml_values['signing_cert']:
            errors['signing_cert'] = {'description': descriptions['signing_cert']}
            if idp_info.get('signing_cert'):
                errors['signing_cert'].update(idp_info['error_codes']['signing_cert'])

        return errors
