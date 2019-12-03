class ResponseBuilder:
    @classmethod
    def construct_response(cls, saml_values, descriptions, errors=None):
        """
        description: Builds final JSON response object
        :type saml_values: dict()
        :type descriptions: dict()
        :type errors: dict()
        :rtype: result: dict()
        """
        result = {}
        for attribute in saml_values:
            result[attribute] = {'value': saml_values.get(attribute)}
            if descriptions.get(attribute):
                result[attribute]['description'] = descriptions.get(attribute)
            if errors.get(attribute):
                result[attribute]['helpx'] = errors.get('helpx')
                result[attribute]['errors_found'] = errors.get(attribute)
        return result
