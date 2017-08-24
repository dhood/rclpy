from collections import OrderedDict

from rcutils import feature_combinations
from rcutils import get_macro_parameters as get_macro_parameters # noqa
from rcutils import severities as severities

# TODO(dhood): support these with lambdas
supported_feature_combinations = \
    OrderedDict(
        {k: v for k, v in feature_combinations.items()
            if 'EXPRESSION' not in k and 'FUNCTION' not in k})
supported_logging_severities = [severity for severity in severities]

# stuff information about wrapping the parameter type
for suffix, feature in supported_feature_combinations.items():
    for param, doc_line in feature.params.items():
        properties = {'doc_line': doc_line} if type(doc_line) == str else doc_line
        properties['scoped_name'] = param
        if param == 'duration':
            properties.update({
                #'scoped_name': 'throttle_duration',
                'scoped_name': 'duration',
                'c_type': 'unsigned PY_LONG_LONG',
                'tuple_type': 'K'})
        if param == 'time_source_type':
            properties.update({
                #'scoped_name': 'throttle_time_source_type',
                'scoped_name': 'time_source_type',
                'c_type': 'const char *',
                'tuple_type': 's'})
        if param == 'name':
            properties.update({
                'c_type': 'const char *',
                'tuple_type': 's'})
        feature.params.update({param: properties})
