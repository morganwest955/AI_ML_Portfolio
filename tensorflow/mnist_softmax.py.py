# Copyright 2015 The TensorFlow Authors. All Rights Reserved.
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

"""A very simple MNIST classifier.

See extensive documentation at
https://www.tensorflow.org/get_started/mnist/beginners
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import sys

from tensorflow.examples.tutorials.mnist import input_data

import tensorflow as tf

FLAGS = None


def main(_):
  # Import data
  mnist = input_data.read_data_sets(FLAGS.data_dir, one_hot=True)

  # Create the model
  x = tf.placeholder(tf.float32, [None, 784])
  W = tf.Variable(tf.zeros([784, 10]))
  b = tf.Variable(tf.zeros([10]))
  y = tf.nn.softmax(tf.matmul(x, W) + b)

  # Define loss and optimizer
  y_ = tf.placeholder(tf.float32, [None, 10])


  #TODO: Add new form of objective here
  log_likelihood = -tf.reduce_mean(tf.log(tf.reduce_sum(y_ * y, reduction_indices=[1])))
  train_step = tf.train.GradientDescentOptimizer(0.05).minimize(log_likelihood)

  correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
  accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
  likelihood = tf.reduce_sum(tf.log(tf.reduce_sum(y_ * y, reduction_indices=[1])))
  
  sess = tf.InteractiveSession()
  tf.global_variables_initializer().run()
  # Train
  for it in range(1000):
    batch_xs, batch_ys = mnist.train.next_batch(100,shuffle=False)

    sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})
    print("Current Accuracy ",sess.run(accuracy, feed_dict={x: mnist.test.images,
                                      y_: mnist.test.labels}))
    print("Batch Likelihood",sess.run(likelihood, feed_dict={x: batch_xs,
                                      y_: batch_ys}))
  # Test trained model
  print("-----------------")
  print("Final Accuracy ",sess.run(accuracy, feed_dict={x: mnist.test.images,
                                      y_: mnist.test.labels}))
  print("Final Likelihood",sess.run(likelihood, feed_dict={x: mnist.test.images,
                                      y_: mnist.test.labels}))

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--data_dir', type=str, default='./tensorflow/mnist/input_data',
                      help='Directory for storing input data')
  FLAGS, unparsed = parser.parse_known_args()
  tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)