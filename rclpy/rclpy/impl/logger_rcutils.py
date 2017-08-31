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


from collections import OrderedDict
try:
    import cPickle as pickle
except ImportError:
    import pickle
import importlib
import inspect
import time

_rclpy_logging = importlib.import_module('._rclpy_logging', package='rclpy')
_rclpy_logging.rclpy_logging_initialize()


def _find_caller(frame):
    # TODO(dhood): make this less hacky
    while 'logger_rcutils' in inspect.getabsfile(frame) \
            or '/logging.py' in inspect.getabsfile(frame):
        frame = frame.f_back
        # print(inspect.getabsfile(frame))
    return frame


def get_caller_id(frame=None):
    if not frame:
        frame = _find_caller(inspect.currentframe())
    return dict(
        function_name=frame.f_code.co_name,
        filename=inspect.getabsfile(frame),
        line_number=frame.f_lineno,
        last_index=frame.f_lasti,  # This is to distinguish between two callers on the same line
    )


class LoggingFilter:
    """Base class for logging filters."""

    """
    Parameters of a filter and their default value, if appropriate.

    A default value of None makes a parameter required.
    """
    params = {}

    """
    Initialize the context of a logging call, e.g. declare variables needed for

    determining the log condition and add them to the context.
    """
    @staticmethod
    def initialize_context(context, **kwargs):
        pass

    """
    Decide if it's appropriate to log given a context, and update the context accordingly.
    """
    @staticmethod
    def log_condition(context):
        return True


class Once(LoggingFilter):
    params = {
        'once': None,
    }

    @staticmethod
    def initialize_context(context, **kwargs):
        context['has_been_logged_once'] = False

    @staticmethod
    def log_condition(context):
        logging_condition = False
        if not context['has_been_logged_once']:
            logging_condition = True
            context['has_been_logged_once'] = True
        return logging_condition


class Throttle(LoggingFilter):
    params = {
        'throttle_duration': None,
        'throttle_time_source_type': 'RCUTILS_STEADY_TIME',
    }

    @staticmethod
    def initialize_context(context, **kwargs):
        context['throttle_duration'] = kwargs['throttle_duration']
        context['throttle_last_logged'] = 0

    @staticmethod
    def log_condition(context):
        logging_condition = True
        # TODO(dhood): use rcutils time and the time source type
        now = time.time()
        logging_condition = now >= context['throttle_last_logged'] + context['throttle_duration']
        if logging_condition:
            context['throttle_last_logged'] = now
        return logging_condition


class SkipFirst(LoggingFilter):
    params = {
        'skip_first': None,
    }

    @staticmethod
    def initialize_context(context, **kwargs):
        context['first_has_been_skipped'] = False

    @staticmethod
    def log_condition(context):
        logging_condition = True
        if not context['first_has_been_skipped']:
            logging_condition = False
            context['first_has_been_skipped'] = True
        return logging_condition


# The ordering of this dictionary matches the order in which filters will be processed.
supported_filters = OrderedDict({
    'throttle': Throttle,
    'skip_first': SkipFirst,
    'once': Once,
})


def get_filters_from_kwargs(**kwargs):
    detected_filters = []
    for filter, filter_class in supported_filters.items():
        if any(kwargs.get(param_name) for param_name in filter_class.params.keys()):
            detected_filters.append(filter)
    # Check that all required parameters (with no default value) have been specified
    for filter in detected_filters:
        for param_name, default_value in supported_filters[filter].params.items():
            if param_name not in kwargs:
                if default_value is not None:
                    kwargs[param_name] = default_value
                else:
                    raise RuntimeError(
                        'required parameter "{0}" not specified '
                        'but is required for the the logging filter "{1}"'.format(
                            param_name, filter))
    # TODO(dhood): warning for unused kwargs
    return detected_filters


class RcutilsLogger:

    _contexts = {}

    def __init__(self, name=''):
        self.name = name

    def get_severity_threshold(self):
        return _rclpy_logging.rclpy_logging_get_severity_threshold()

    def set_severity_threshold(self, severity):
        return _rclpy_logging.rclpy_logging_set_severity_threshold(severity)

    def log(self, message, severity, **kwargs):
        caller_id = get_caller_id()
        caller_id_str = pickle.dumps(caller_id)
        # Get/prepare the context corresponding to the caller.
        if caller_id_str not in self._contexts:
            # Infer the requested log filters from the keyword arguments
            detected_filters = get_filters_from_kwargs(**kwargs)

            name = kwargs.get('name', self.name)
            context = {'name': name, 'severity': severity}
            for filter in detected_filters:
                if filter in supported_filters:
                    supported_filters[filter].initialize_context(context, **kwargs)
            context['filters'] = detected_filters
            self._contexts[caller_id_str] = context
        context = self._contexts[caller_id_str]

        # Determine if it's appropriate to process the message (any filter can vote no)
        make_log_call = True
        for filter in context['filters']:
            if filter in supported_filters and make_log_call:
                make_log_call &= supported_filters[filter].log_condition(
                    self._contexts[caller_id_str])
        if make_log_call:
            # Get the relevant function from the C extension
            log_function = getattr(_rclpy_logging, 'rclpy_logging_log_' + severity.name.lower())
            log_function(
                context['name'], message,
                caller_id['function_name'], caller_id['filename'], caller_id['line_number'])