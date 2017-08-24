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

import rclpy.impl.logging_rcutils


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

    def short_form(self):
        if self.name == 'RCLPY_LOG_SEVERITY_DEBUG':
            return 'debug'
        if self.name == 'RCLPY_LOG_SEVERITY_INFO':
            return 'info'
        if self.name == 'RCLPY_LOG_SEVERITY_WARN':
            return 'warn'
        if self.name == 'RCLPY_LOG_SEVERITY_ERROR':
            return 'error'
        if self.name == 'RCLPY_LOG_SEVERITY_FATAL':
            return 'fatal'


def initialize():
    return rclpy.impl.logging_rcutils.initialize()


def get_severity_threshold():
    return rclpy.impl.logging_rcutils.get_severity_threshold()


def set_severity_threshold(severity):
    assert isinstance(severity, LoggingSeverity) or isinstance(severity, int)
    return rclpy.impl.logging_rcutils.set_severity_threshold(severity)


def logdebug(message):
    return log(message, severity=LoggingSeverity.RCLPY_LOG_SEVERITY_INFO)


def loginfo(message):
    return log(message, severity=LoggingSeverity.RCLPY_LOG_SEVERITY_INFO)


def logwarn(message):
    return log(message, severity=LoggingSeverity.RCLPY_LOG_SEVERITY_WARN)


def logerr(message):
    return log(message, severity=LoggingSeverity.RCLPY_LOG_SEVERITY_ERROR)


def logfatal(message):
    return log(message, severity=LoggingSeverity.RCLPY_LOG_SEVERITY_FATAL)


def log(message, severity, **kwargs):
    assert isinstance(severity, LoggingSeverity) or isinstance(severity, int)
    severity = LoggingSeverity(severity)

    return rclpy.impl.logging_rcutils.log(message, severity, **kwargs)
