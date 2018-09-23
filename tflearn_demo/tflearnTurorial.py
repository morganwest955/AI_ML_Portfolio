# -*- coding: utf-8 -*-

""" Auto Encoder Example.

Using an auto encoder on MNIST handwritten digits.

References:
    Y. LeCun, L. Bottou, Y. Bengio, and P. Haffner. "Gradient-based
    learning applied to document recognition." Proceedings of the IEEE,
    86(11):2278-2324, November 1998.

Links:
    [MNIST Dataset] http://yann.lecun.com/exdb/mnist/

"""
from __future__ import division, print_function, absolute_import

import numpy as np
import matplotlib.pyplot as plt
import tflearn
import tflearn.datasets.oxflower17 as oxflower17
import time

# Data loading and preprocessing
import tflearn.datasets.mnist as mnist

X, Y = oxflower17.load_data(one_hot=True, resize_pics=(28, 28))
X = np.reshape(X, (len(X),2352))
testX = X[1000:]
X = X[:1000]
start_time = time.time()


# Building the encoder
encoder = tflearn.input_data(shape=[None, 2352])
encoder = tflearn.fully_connected(encoder, 2100)
encoder = tflearn.fully_connected(encoder, 200)

# Building the decoder
decoder = tflearn.fully_connected(encoder, 2100)
decoder = tflearn.fully_connected(decoder, 2352, activation='sigmoid')

# Regression, with mean square error
net = tflearn.regression(decoder, optimizer='adam', learning_rate=0.001,
                         loss='mean_square', metric=None)

# Training the auto encoder
model = tflearn.DNN(net, tensorboard_verbose=0)
model.fit(X, X, n_epoch=150, validation_set=(testX, testX),
          run_id="auto_encoder", batch_size=256)

# Encoding X[0] for test
print("\nTest encoding of X[0]:")
# New model, re-using the same session, for weights sharing
encoding_model = tflearn.DNN(encoder, session=model.session)
print(encoding_model.predict([X[0]]))

# Testing the image reconstruction on new data (test set)
print("\nVisualizing results after being encoded and decoded:")
testX = tflearn.data_utils.shuffle(testX)[0]
# Applying encode and decode over test set
encode_decode = model.predict(testX)
# Compare original images with their reconstructions
f, a = plt.subplots(2, 10, figsize=(10, 2))
for i in range(10):
    temp = testX[i]
    a[0][i].imshow(np.reshape(temp, (28, 28, 3)))
    temp = encode_decode[i]
    a[1][i].imshow(np.reshape(temp, (28, 28, 3)))
print("--- %s seconds ---" % (time.time() - start_time))
f.show()
plt.draw()
plt.waitforbuttonpress()

