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

import rclpy.rcutils
from rclpy.rcutils import feature_combinations


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


def log(
        message, severity=LoggingSeverity.RCLPY_LOG_SEVERITY_INFO, *,
        name=None, once=False, throttle_duration=None, throttle_time_source_type=None):
    suffix = ''
    # Build up the suffix
    if throttle_duration or throttle_time_source_type:
        suffix += '_THROTTLE'
    if once:
        suffix += '_ONCE'
    if name:
        suffix += '_NAMED'
    if suffix not in rclpy.rcutils.feature_combinations:
        raise AttributeError('invalid logging combination')
    # Get the ordered dict for that suffix (maintaining ordering is important)
    args = rclpy.rcutils.get_macro_parameters(suffix)
    if throttle_duration or throttle_time_source_type:
        args['duration'] = throttle_duration
        args['time_source_type'] = throttle_time_source_type
    if once:
        args['name'] = name
    if name:
        args['name'] = name
    required_params = rclpy.rcutils.get_macro_parameters(suffix)
    for p in required_params:
        if p not in args.keys() or args[p] is None:
            raise RuntimeError('required parameter {0} not specified but required for logging {1}'.format(p, suffix))
    print(suffix)
    print(args)
    return
