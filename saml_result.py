class SamlResult:
    def __init__(self, analysis_values, descriptions, errors=None):
        self.result = self.construct_result(analysis_values, descriptions, errors)

    def construct_result(self, analysis_values, descriptions, errors):
        result = {}
        #result['errors_found'] = {}
        for each in analysis_values:
            result[each] = {}
            result[each]['value'] = analysis_values[each]
            if descriptions.get(each):
                result[each]['description'] = descriptions[each]
            if errors.get(each):
                #result['errors_found'][each] = errors[each]
                result[each]['errors_found'] = errors[each]
        return result

