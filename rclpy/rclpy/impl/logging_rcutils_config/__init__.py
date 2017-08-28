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


import rcutils
from rcutils import feature_combinations
from rcutils import get_suffix_from_features as get_suffix_from_features # noqa
from rcutils import severities as severities

# TODO(dhood): support these with lambdas
supported_feature_combinations = \
    {k: v for k, v in feature_combinations.items()
        if 'EXPRESSION' not in k and 'FUNCTION' not in k}
supported_logging_severities = [severity for severity in severities]

# stuff information about wrapping the parameter type
for suffix, feature in supported_feature_combinations.items():
    for param, doc_line in feature.params.items():
        properties = {'doc_line': doc_line} if type(doc_line) == str else doc_line
        properties['scoped_name'] = param
        if param == 'skipfirst':
            properties.update({
                'scoped_name': 'throttle_duration',
            })
        if param == 'duration':
            properties.update({
                'scoped_name': 'throttle_duration',
                'c_type': 'PY_LONG_LONG',
                'tuple_type': 'K',
            })
        if param == 'time_source_type':
            properties.update({
                'scoped_name': 'throttle_time_source_type',
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
    macro_parameters = rcutils.get_macro_parameters(suffix)
    return macro_parameters


def get_features_from_kwargs(**kwargs):
    features = []
    if kwargs.get('skip_first'):
        features.append('skip_first')
    if kwargs.get('throttle_duration') or kwargs.get('throttle_time_source_type'):
        features.append('throttle')
    if kwargs.get('once'):
        features.append('once')
    if kwargs.get('name'):
        features.append('named')

    # TODO(dhood): warning for unused kwargs?
    return features
