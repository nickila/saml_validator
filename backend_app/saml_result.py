class SamlResult:
    @classmethod
    def construct_result(cls, saml_values, descriptions, errors=None):
        result = {}
        for each in saml_values:
            result[each] = {}
            result[each]['value'] = saml_values[each]
            if descriptions.get(each):
                result[each]['description'] = descriptions[each]
            if errors.get(each):
                result[each]['errors_found'] = errors[each]
        return result

