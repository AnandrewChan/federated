# Copyright 2018, The TensorFlow Federated Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""General utilities specific to the manipulation of tensors and operators."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Dependency imports
import tensorflow as tf

# TODO(b/118783928) Fix BUILD target visibility.
from tensorflow.python.framework import tensor_util

from tensorflow_federated.python.common_libs import py_typecheck


def is_scalar(tensor):
  """Returns True iff the given tensor is a scalar.

  Args:
    tensor: The tensor to test for being a scalar.

  Returns:
    True if 'tensor' is a scalar, i.e. all dims are 1, False otherwise.

  Raises:
    TypeError: when the argument is not a tensor.
  """
  if not tensor_util.is_tensor(tensor):
    raise TypeError('Expected a tensor, found "{}".'.format(
        py_typecheck.type_string(type(tensor))))
  return (hasattr(tensor, 'get_shape') and
          all(dim == 1 for dim in tensor.get_shape()))


def metrics_sum(values, name=None):
  """A function like tf.metrics.mean, but for a simple sum.

  Args:
    values: A rank-1 tensor to be summed.
    name: Optional name for the op.

  Returns:
    A tuple of:
      sum: A variable holding the current sum of all 'values' seen so far.
      update_op: An opt to run on each minibatch.
  """
  with tf.variable_scope(name, 'metrics_sum', (values,)):
    sum_var = tf.get_variable(
        'sum', [], values.dtype,
        initializer=tf.zeros_initializer,
        collections=[tf.GraphKeys.LOCAL_VARIABLES],
        trainable=False)
    update_op = tf.assign_add(sum_var, tf.reduce_sum(values))
    return sum_var, update_op
