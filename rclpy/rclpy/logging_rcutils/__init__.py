from collections import OrderedDict

from rclpy.impl.implementation_singleton import rclpy_logging_implementation as _rclpy_logging

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


def initialize():
    return _rclpy_logging.rclpy_logging_initialize()


def get_severity_threshold():
    return _rclpy_logging.rclpy_logging_get_severity_threshold()


def set_severity_threshold(severity):
    return _rclpy_logging.rclpy_logging_set_severity_threshold(severity)


def log(message, severity, **kwargs):
    # Build up the suffix
    suffix = ''
    if kwargs.get('skipfirst'):
        suffix += '_SKIPFIRST'
    if kwargs.get('duration') or kwargs.get('time_source_type'):
        suffix += '_THROTTLE'
    if kwargs.get('once'):
        suffix += '_ONCE'
    if kwargs.get('name'):
        suffix += '_NAMED'

    if suffix not in supported_feature_combinations:
        raise AttributeError('invalid combination of logging features')

    required_params = get_macro_parameters(suffix)
    # Copy only the required arguments into a minimal dictionary
    # TODO(dhood): make c functions ignore unnecessary keyword arguments
    params = {}
    for p in required_params:
        try:
            params[p] = kwargs[p]
        except:
            raise RuntimeError(
                'required parameter "{0}" not specified '
                'but required for logging feature "{1}"'.format(p, suffix))
    f = getattr(_rclpy_logging, 'rclpy_logging_log_' + severity.short_form() + suffix.lower())
    return f(message, **params)
