class SamlResult:
    def __init__(self, analysis_values, errors=None):
        self.values = self.construct_result(analysis_values, errors)

    def construct_result(self, analysis_values, errors):
        result = {}
        result['errors_found'] = {}
        for each in analysis_values:
            if each in errors:
                result['errors_found'][each] = errors[each]
            result[each] = analysis_values[each]
        return result

