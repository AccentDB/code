
from __future__ import print_function
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from time import time
#np.random.seed(1337)  # for reproducibility

from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.normalization import BatchNormalization
from keras.layers.convolutional import Convolution1D, MaxPooling1D
from keras.utils import np_utils
from keras.callbacks import TensorBoard


# set parameters:
test_dim = 2999
maxlen = 100
nb_filter = 64
filter_length_1 = 50
filter_length_2 = 25
hidden_dims = 250
nb_epoch = 20
nb_classes = 2
split_ratio = 0.15

print('Loading data...')

X = np.load('../data/numpy_vectors/x_label_splits.npy')
y = np.load('../data/numpy_vectors/y_label_splits.npy')
print(X.shape)
print(y.shape)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=split_ratio)

xts = X_train.shape
#X_train = np.reshape(X_train, (xts[0], xts[1], 1))
xtss = X_test.shape
#X_test = np.reshape(X_test, (xtss[0], xtss[1], 1))
yts = y_train.shape
#y_train = np.reshape(y_train, (yts[0], 1))
ytss = y_test.shape
#y_test = np.reshape(y_test, (ytss[0], 1))

print(len(X_train), 'train sequences')
print(len(X_test), 'test sequences')

Y_train = np_utils.to_categorical(y_train, nb_classes)
Y_test = np_utils.to_categorical(y_test, nb_classes)

# print('Pad sequences (samples x time)')
# X_train = sequence.pad_sequences(X_train, maxlen=maxlen)
# X_test = sequence.pad_sequences(X_test, maxlen=maxlen)
# print('X_train shape:', X_train.shape)
# print('X_test shape:', X_test.shape)

for batch_size in range(10, 11, 5):
    print('Build model...')
    model = Sequential()

    # we start off with an efficient embedding layer which maps
    # our vocab indices into embedding_dims dimensions
    # model.add(Embedding(max_features, embedding_dims, input_length=maxlen))
    # model.add(Dropout(0.25))

    # we add a Convolution1D, which will learn nb_filter
    # word group filters of size filter_length:
    model.add(Convolution1D(nb_filter=nb_filter,
                            filter_length=filter_length_1,
                            input_shape=(test_dim, 13),
                            border_mode='valid',
                            activation='relu'
                            ))
    # we use standard max pooling (halving the output of the previous layer):
    model.add(BatchNormalization())

    model.add(Convolution1D(nb_filter=nb_filter,
                            filter_length=filter_length_2,
                            border_mode='same',
                            activation='relu'
                            ))

    model.add(BatchNormalization())

    model.add(MaxPooling1D(pool_length=2))

    model.add(Convolution1D(nb_filter=nb_filter,
                            filter_length=filter_length_2,
                            border_mode='same',
                            activation='relu'
                            ))

    model.add(BatchNormalization())

    model.add(MaxPooling1D(pool_length=2))

    # We flatten the output of the conv layer,
    # so that we can add a vanilla dense layer:
    model.add(Flatten())

    # We add a vanilla hidden layer:
    # model.add(Dense(hidden_dims))
    model.add(Dropout(0.25))
    # model.add(Activation('relu'))

    # We project onto a single unit output layer, and squash it with a sigmoid:
    model.add(Dense(nb_classes))
    model.add(Activation('softmax'))

    model.compile(loss='binary_crossentropy',
                optimizer='adam', metrics=['accuracy'])

    print("model/split = {} <> batchsize = {}".format(split_ratio, batch_size))
    tensorboard = TensorBoard(log_dir="logs/split_{}_batchsize_{}".format(split_ratio, batch_size))

    model.fit(X_train, Y_train, batch_size=batch_size,
            nb_epoch=nb_epoch,  verbose=1, callbacks=[tensorboard]	)

    # model.save('model_hin_tel_38_samples.h5')

    y_preds = model.predict(X_test)
    for i in range(len(y_preds)):
        print(y_preds[i], y_test[i])
        
    score = model.evaluate(X_test, Y_test, verbose=1)
    print(score)
    print("\n**********************************\n")

# print(classification_report(Y_test, Y_preds))
