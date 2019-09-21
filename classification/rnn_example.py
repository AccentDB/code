from __future__ import print_function
import numpy as np

from .attention_lstm import goo
from keras.optimizers import SGD


np.random.seed(1337)  # for reproducibility
from keras.preprocessing import sequence
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.recurrent import LSTM
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report
from gen_y import generate_y

hidden_units = 100
nb_classes = 2
print('Loading data...')
X = np.load('x_test_mfcc_split_wav_30sec.npy')
y = generate_y('/media/enigmaeth/My Passport/Datasets/linguistics data/split_wav_30sec')

X = X[:200]
y = y[:200]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)
batch_size = 20

split__ = int((len(X_train)//batch_size)*batch_size)
X_train = X_train[:split__]
y_train = y_train[:split__]


print(len(X_train), 'train sequences')
print(len(X_test), 'test sequences')
print('X_train shape:', X_train.shape)
print('X_test shape:', X_test.shape)
print('y_train shape:', y_train.shape)
print('y_test shape:', y_test.shape)
print('Build model...')

print(y_train)
Y_train = np_utils.to_categorical(y_train, nb_classes)
Y_test = np_utils.to_categorical(y_test, nb_classes)

model = Sequential()

#batch_input_shape= (batch_size, X_train.shape[1], X_train.shape[2])

# note that it is necessary to pass in 3d batch_input_shape if stateful=True
model.add(LSTM(64, return_sequences=True, stateful=False,
               batch_input_shape= (batch_size, X_train.shape[1], X_train.shape[2])))
model.add(LSTM(64, return_sequences=True, stateful=False))
model.add(LSTM(64, stateful=False))


# add dropout to control for overfitting
model.add(Dropout(.25))

# squash output onto number of classes in probability space
model.add(Dense(nb_classes, activation='softmax'))


model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=["accuracy"])

print("Train...")
model.fit(X_train, Y_train, batch_size=batch_size, epochs=5, validation_data=(X_test, Y_test))

y_pred=model.predict_classes(X_test, batch_size=batch_size)
print(classification_report(y_test, y_pred))

model.save('model_5epochs_rnn.h5')
