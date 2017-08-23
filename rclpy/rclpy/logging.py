# Copyright 2017 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from enum import IntEnum

from rclpy.impl.implementation_singleton import rclpy_logging_implementation as _rclpy_logging

import rcutils


class LoggingSeverity(IntEnum):
    """
    Enum for logging severity levels.

    This enum matches the one defined in rcutils/logging.h
    """

    RCLPY_LOG_SEVERITY_DEBUG = 0
    RCLPY_LOG_SEVERITY_INFO = 1
    RCLPY_LOG_SEVERITY_WARN = 2
    RCLPY_LOG_SEVERITY_ERROR = 3
    RCLPY_LOG_SEVERITY_FATAL = 4


def initialize():
    return _rclpy_logging.rclpy_logging_initialize()


def get_severity_threshold():
    return _rclpy_logging.rclpy_logging_get_severity_threshold()


def set_severity_threshold(severity):
    assert isinstance(severity, LoggingSeverity) or isinstance(severity, int)
    return _rclpy_logging.rclpy_logging_set_severity_threshold(severity)


def logdebug(message):
    return _rclpy_logging.rclpy_logging_log_debug(message)


def loginfo(message):
    log(message, severity=LoggingSeverity.RCLPY_LOG_SEVERITY_INFO)


def logwarn(message):
    log(message, severity=LoggingSeverity.RCLPY_LOG_SEVERITY_WARN)


# TODO(dhood): make logerr
def logerror(message):
    log(message, severity=LoggingSeverity.RCLPY_LOG_SEVERITY_ERROR)


def logfatal(message):
    log(message, severity=LoggingSeverity.RCLPY_LOG_SEVERITY_FATAL)

'''
# using an input of duration instead of throttle_duration
param_mappings = {
    'duration': 'throttle_duration',
    'time_source_type': 'duration_time_source_type'
}

required_params = {}
for suffix in rclpy.rcutils.feature_combinations:
    required_params_suffix = rclpy.rcutils.feature_combinations[suffix].params
    for param, desc in required_params_suffix:
        if param in param_mappings:
            required_params_suffix[param_mappings[p]] = desc
    required_params[suffix] = required_params_suffix
'''


def log(message, severity, **kwargs):
    assert isinstance(severity, LoggingSeverity) or isinstance(severity, int)
    suffix = ''

    # Build up the suffix
    if 'duration' in kwargs or 'time_source_type' in kwargs:
        suffix += '_THROTTLE'
    if 'once' in kwargs:
        suffix += '_ONCE'
    if 'name' in kwargs:
        suffix += '_NAMED'

    if suffix not in rcutils.feature_combinations:
        raise AttributeError('invalid combination of logging features')

    # Get the ordered dict for that suffix (maintaining ordering is important)
    args = rcutils.get_macro_parameters(suffix)
    required_params = rcutils.get_macro_parameters(suffix)
    for p in required_params:
        if p not in kwargs:
            raise RuntimeError('required parameter {0} not specified but required for logging {1}'.format(p, suffix))
    print(suffix)
    print(args)
    return
