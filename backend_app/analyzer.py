from backend_app.response_builder import ResponseBuilder
from backend_app.error_handler import SamlParsingError


class Analyzer:
    @classmethod
    def process(cls, saml_dict, descriptions, idp_info):
        saml_values = cls.parse_saml(saml_dict)
        errors = cls.create_error_dict(saml_values, descriptions.get('error_message'), idp_info)
        return ResponseBuilder.construct_response(saml_values, descriptions.get('metadata'), errors)

    @classmethod
    def parse_saml(cls, dict_saml_trace):
        """
        desciption: This method extracts the saml attributes we are targeting for analysis
        :type dict_saml_trace: dict(result of xmltodict.parse(uploaded XML file))
        :rtype: saml_trace_values: dict(extracted saml values)
        """
        try:
            first_key = list(dict_saml_trace)[0]
            key = 'saml2' if '2' in first_key else 'saml'
            dict_saml_trace = dict_saml_trace[key + 'p:Response']
            signature = dict_saml_trace['ds:Signature']
            assertions = dict_saml_trace[key + ':Assertion']
        except Exception as e:
            raise SamlParsingError('Error parsing uploaded file ' + str(e))
        saml_trace_values = {}
        attributes_released = cls.get_attribute_value(assertions, [key + ':AttributeStatement', key + ':Attribute'])
        if attributes_released:
            assertion_attributes = {}
            for each in attributes_released:
                try:
                    assertion_attributes[each['@Name']] = each[key + ':AttributeValue']['#text']
                except:
                    assertion_attributes[each['@Name']] = None
            saml_trace_values['assertion_attributes'] = assertion_attributes
        else:
            saml_trace_values['assertion_attributes'] = None

        saml_trace_values['name_id'] = cls.get_attribute_value(assertions, [key + ':Subject', key + ':NameID', '#text'])
        saml_trace_values['name_id_format'] = cls.get_attribute_value(assertions,
                                                                      [key + ':Subject', key + ':NameID', '@Format'])
        saml_trace_values['destination'] = cls.get_attribute_value(dict_saml_trace, ['@Destination'])
        saml_trace_values['issuer_url'] = cls.get_attribute_value(assertions,
                                                                  [key + ':Conditions', key + ':AudienceRestriction',
                                                                   key + ':Audience'])
        saml_trace_values['signature_method_algorithm'] = cls.get_attribute_value(signature, ['ds:SignedInfo',
                                                                                              'ds:SignatureMethod',
                                                                                              '@Algorithm'])
        saml_trace_values['digest_method_algorithm'] = cls.get_attribute_value(signature,
                                                                               ['ds:SignedInfo', 'ds:Reference',
                                                                                'ds:DigestMethod', '@Algorithm'])
        saml_trace_values['not_before'] = cls.get_attribute_value(assertions, [key + ':Conditions', '@NotBefore'])
        saml_trace_values['time_sent'] = cls.get_attribute_value(dict_saml_trace, ['@IssueInstant'])
        saml_trace_values['not_on_or_after'] = cls.get_attribute_value(assertions,
                                                                       [key + ':Conditions', '@NotOnOrAfter'])
        saml_trace_values['signing_cert'] = cls.get_attribute_value(signature,
                                                                    ['ds:KeyInfo', 'ds:X509Data', 'ds:X509Certificate'])
        saml_trace_values['in_response_to'] = cls.get_attribute_value(dict_saml_trace, ['@InResponseTo'])

        if all(value is None for value in saml_trace_values.values()):
            raise SamlParsingError('Issues Parsing dict(XML), Saml values were unable to be extracted')
        return saml_trace_values

    @classmethod
    def get_attribute_value(cls, section, keys):
        """
        description: retrieve value/s at given key location
        :type section: dict()
        :type keys: list(index keys)
        :rtype: value: str() or dict()
        """
        try:
            value = section
            for k in keys:
                value = value[k]
        except:
            value = None
        return value

    @classmethod
    def create_error_dict(cls, saml_values, descriptions, idp_info={}):
        """
        description: Compares saml values with the common errors below
        :type saml_values: dict(parsed saml values from xml upload)
        :type descriptions: dict(metadata from resources/descriptions.yml)
        :type idp_info: dict(session specific idp info from resources/idp.yml )
        :rtype: errors dict(saml errors found)
        """
        errors = {}
        idp_info = idp_info.get('error_codes', {})
        # Checks if assertion attributes are being released
        if not saml_values['assertion_attributes']:
            errors['assertion_attributes'] = {'description': descriptions['no_attributes']}
            if idp_info.get('assertion_attributes'):
                errors['assertion_attributes'].update(idp_info['assertion_attributes'])
        else:
            # Checks if FirstName, LastName, and Email attributes are being released and are labeled correctly
            if not {'FirstName', 'LastName', 'Email'}.issubset(saml_values['assertion_attributes']):
                errors['assertion_attributes'] = {
                    'description': descriptions['assertion_attributes']}
                if idp_info.get('assertion_attributes'):
                    errors['assertion_attributes'].update(idp_info['assertion_attributes'])
        # Checks for presence of name-id
        if not saml_values['name_id']:
            errors['name_id'] = {'descriptions': descriptions['name_id']}
            if idp_info.get('name_id'):
                errors['name_id'].update(idp_info['name_id'])
        # Checks if name-id format is either unspecified or emailAddress
        name_id_format = saml_values['name_id_format']
        if 'unspecified' not in name_id_format and 'emailAddress' not in name_id_format:
            errors['name_id_format'] = {'description': descriptions['name_id_format']}
            if idp_info.get('name_id_format'):
                errors['name_id_format'].update(idp_info['name_id_format'])
        # Checks for presence of token signing certificate
        if not saml_values['signing_cert']:
            errors['signing_cert'] = {'description': descriptions['signing_cert']}
            if idp_info.get('signing_cert'):
                errors['signing_cert'].update(idp_info['signing_cert'])
        # Checks for presence of InResponseTo attribute
        if not saml_values['in_response_to']:
            errors['in_response_to'] = {'description': descriptions['in_response_to']}
        return errors
