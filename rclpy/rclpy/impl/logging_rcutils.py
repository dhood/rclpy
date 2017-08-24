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


from rclpy.impl.implementation_singleton import rclpy_logging_implementation as _rclpy_logging
import rclpy.logging_rcutils


def initialize():
    return _rclpy_logging.rclpy_logging_initialize()


def get_severity_threshold():
    return _rclpy_logging.rclpy_logging_get_severity_threshold()


def set_severity_threshold(severity):
    return _rclpy_logging.rclpy_logging_set_severity_threshold(severity)


def log(message, severity, **kwargs):
    # Build up the suffix
    suffix = ''
    if kwargs.get('skip_first'):
        suffix += '_SKIPFIRST'
    if kwargs.get('throttle_duration') or kwargs.get('throttle_time_source_type'):
        suffix += '_THROTTLE'
    if kwargs.get('once'):
        suffix += '_ONCE'
    if kwargs.get('name'):
        suffix += '_NAMED'

    if suffix not in rclpy.logging_rcutils.supported_feature_combinations:
        raise AttributeError('invalid combination of logging features')

    required_params = rclpy.logging_rcutils.get_macro_parameters(suffix)
    # Copy only the required arguments into a minimal dictionary
    # TODO(dhood): make c functions ignore unnecessary keyword arguments
    params = {}
    for p, properties in required_params.items():
        scoped_name = properties['scoped_name']
        try:
            params[scoped_name] = kwargs[scoped_name]
        except:
            raise RuntimeError(
                'required parameter "{0}" not specified '
                'but required for logging feature "{1}"'.format(scoped_name, suffix))
    f = getattr(_rclpy_logging, 'rclpy_logging_log_' + severity.short_form() + suffix.lower())
    return f(message, **params)
