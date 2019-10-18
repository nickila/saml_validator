class SamlResult:
    @classmethod
    def construct_result(cls, saml_values, descriptions, errors=None):
        result = {}
        for attribute in saml_values:
            result[attribute] = {'value': saml_values[attribute]}
            if descriptions.get('metadata').get(attribute):
                result[attribute]['description'] = descriptions['metadata'][attribute]
            if errors.get(attribute):
                result[attribute]['errors_found'] = errors[attribute]
        return result
