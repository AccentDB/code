from __future__ import print_function
import numpy as np

from keras.optimizers import SGD
from keras.callbacks import TensorBoard

np.random.seed(1337)  # for reproducibility
from keras.preprocessing import sequence
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Bidirectional
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.recurrent import LSTM
from keras.layers.convolutional import Convolution1D, MaxPooling1D
from keras.layers.normalization import BatchNormalization
from keras.preprocessing import sequence
from keras.utils import np_utils
from keras.layers.core import Dense, Dropout, Activation, Flatten

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from gen_y import generate_y

# parameters
test_dim = 2999
maxlen = 100
batch_size = 100
nb_filter = 64
filter_length_1 = 50
filter_length_2 = 25
hidden_dims = 250
nb_epoch = 4
nb_classes = 2

print('Loading data...')
X = np.load('x_test_mfcc_eng_mand_equal.npy')
print(X.shape)
y = generate_y('/media/enigmaeth/My Passport/Datasets/linguistics data/eng_mand_equal')
print(y.shape)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15)

print(len(X_train), 'train sequences')
print(len(X_test), 'test sequences')

Y_train = np_utils.to_categorical(y_train, nb_classes)
Y_test = np_utils.to_categorical(y_test, nb_classes)

# create the model
embedding_vecor_length = 32
model = Sequential()

# model.add(Conv1D(filters=32, input_shape=(test_dim, 13), kernel_size=3, padding='same', activation='relu'))
model.add(Convolution1D(nb_filter=nb_filter,
                        filter_length=filter_length_1,
                        input_shape=(test_dim, 13),
                        border_mode='valid',
                        activation='relu'
                        ))

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

# We add a vanilla hidden layer:
# model.add(Dense(hidden_dims))
model.add(Dropout(0.25))

model.add(Bidirectional(LSTM(100, return_sequences=True)))
model.add(Bidirectional(LSTM(100, return_sequences=True)))
model.add(Bidirectional(LSTM(100)))

model.add(Dropout(0.25))

model.add(Dense(128, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(nb_classes, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

print(model.summary())

model.fit(X_train, Y_train, batch_size=batch_size,
        nb_epoch=nb_epoch,  verbose=1, validation_split=0.15)

y_preds = model.predict(X_test)
for i in range(len(y_preds)):
	print(y_preds[i], y_test[i])
	# Final evaluation of the model
scores = model.evaluate(X_test, Y_test, verbose=0)
print("Accuracy: %.2f%%" % (scores[1]*100))
