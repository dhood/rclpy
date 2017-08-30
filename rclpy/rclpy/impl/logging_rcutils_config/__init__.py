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

from copy import deepcopy

import rcutils
from rcutils.logging import get_suffix_from_features as get_suffix_from_features # noqa
from rcutils.logging import severities as severities

supported_feature_combinations = \
    {k: deepcopy(v) for k, v in rcutils.logging.feature_combinations.items()
        # TODO(dhood): support these with lambdas
        if 'EXPRESSION' not in k and 'FUNCTION' not in k}
supported_logging_severities = severities

# Stuff information about each parameter needed for the C extension
for suffix, feature in supported_feature_combinations.items():
    for param, doc_line in feature.params.items():
        properties = {'doc_line': doc_line}
        properties['scoped_name'] = param
        if param == 'skipfirst':
            properties.update({
                'scoped_name': 'throttle_duration',
            })
        if param == 'duration':
            properties.update({
                'scoped_name': 'throttle_duration',
                'c_type': 'rcutils_duration_value_t',
                'tuple_type': 'K',
            })
        if param == 'time_source_type':
            properties.update({
                'scoped_name': 'throttle_time_source_type',
                # TODO(dhood): update to pass a capsule of the time source,
                # once it's being used in the throttle feature in rcutils
                'c_type': 'const char *',
                'tuple_type': 's',
            })
        if param == 'name':
            properties.update({
                'c_type': 'const char *',
                'tuple_type': 's',
            })
        feature.params.update({param: properties})


def get_macro_parameters(suffix):
    return supported_feature_combinations[suffix].params


def get_features_from_kwargs(**kwargs):
    detected_features = []
    for feature, feature_class in feature_classes.items():
        if any(kwargs.get(param_name) for param_name in feature_class.params.keys()):
            detected_features.append(feature)
    # Check that all required parameters (with no default value) have been specified
    for feature in detected_features:
        for param_name, default_value in feature_classes[feature].params.items():
            if param_name not in kwargs:
                if default_value is not None:
                    kwargs[param_name] = default_value
                else:
                    raise RuntimeError(
                        'required parameter "{0}" not specified '
                        'but is required for the the logging feature "{1}"'.format(
                            param_name, feature))
    # TODO(dhood): warning for unused kwargs?
    return detected_features
