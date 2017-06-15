# Copyright 2016 The TensorFlow Authors. All Rights Reserved.
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
# ==============================================================================
"""TensorBoard Plugin abstract base class.

Every plugin in TensorBoard must extend and implement the abstract methods of
this base class.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections

from abc import ABCMeta
from abc import abstractmethod


class TBPlugin(object):
  """TensorBoard plugin interface. Every plugin must extend from this class.

  Subclasses must have a constructor that takes a TBContext argument.
  """
  __metaclass__ = ABCMeta

  # The plugin_name will also be a prefix in the http handlers generated by
  # the plugin, e.g. `data/plugins/$PLUGIN_NAME/$HANDLER`
  # The plugin name must be unique for each registered plugin, or
  # a ValueError will be thrown when the application is constructed. The
  # plugin name must only contain characters among [A-Za-z0-9_.-], and
  # must be nonempty, or a ValueError will similarly be thrown.
  plugin_name = None

  @abstractmethod
  def get_plugin_apps(self):
    """Returns a set of WSGI applications that the plugin implements.

    Each application gets registered with the tensorboard app and is served
    under a prefix path that includes the name of the plugin.

    Returns:
      A dict mapping route paths to WSGI applications. Each route path
      should include a leading slash.
    """
    raise NotImplementedError()

  @abstractmethod
  def is_active(self):
    """Determines whether this plugin is active.

    A plugin may not be active for instance if it lacks relevant data. If a
    plugin is inactive, the frontend may avoid issuing requests to its routes.

    Returns:
      A boolean value. Whether this plugin is active.
    """
    raise NotImplementedError()


class TBContext(collections.namedtuple('TBContext', ('logdir', 'multiplexer'))):
  """Magic container of information passed from TensorBoard core to plugins.

  A TBContext instance is passed to the constructor of a TBPlugin class.

  Fields:
    logdir: The string logging directory TensorBoard was started with.
    multiplexer: An EventMultiplexer with underlying TB data, or None if SQL
        mode is being used.
  """
  __slots__ = ()  # Enforces use of only tuple fields.
