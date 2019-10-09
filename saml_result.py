class SamlResult:
    @classmethod
    def construct_result(cls, analysis_values, descriptions, errors=None):
        result = {}
        for each in analysis_values:
            result[each] = {}
            result[each]['value'] = analysis_values[each]
            if descriptions.get(each):
                result[each]['description'] = descriptions[each]
            if errors.get(each):
                result[each]['errors_found'] = errors[each]
        return result

