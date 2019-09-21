from __future__ import print_function
from keras.layers import multiply
from keras.layers.core import *
from keras.layers.recurrent import LSTM
from keras.models import *

import numpy as np

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

from attention_utils import get_activations, get_data_recurrent
nb_classes = 2
INPUT_DIM = 13
TIME_STEPS = 2999
# if True, the attention vector is shared across the input_dimensions where the attention is applied.
SINGLE_ATTENTION_VECTOR = False
APPLY_ATTENTION_BEFORE_LSTM = True


print('Loading data...')
X = np.load('x_test_mfcc_eng_mandarin.npy')
y = generate_y('/media/enigmaeth/My Passport/Datasets/linguistics data/eng_mandarin')
N = X.shape[0]
X = X.repeat(2).repeat(2)
y = y.repeat(2).repeat(2)
X = X.reshape(4*N, 2999, 13)
print(X.shape)

#X = X[:200]
#y = y[:200]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10)
batch_size = 50

Y_train = np_utils.to_categorical(y_train, nb_classes)
Y_test = np_utils.to_categorical(y_test, nb_classes)
#split__ = int((len(X_train)//batch_size)*batch_size)
#X_train = X_train[:split__]
#y_train = y_train[:split__]

def attention_3d_block(inputs):
	# inputs.shape = (batch_size, time_steps, input_dim)
	input_dim = int(inputs.shape[2])
	a = Permute((2, 1))(inputs)
	a = Reshape((input_dim, TIME_STEPS))(a) # this line is not useful. It's just to know which dimension is what.
	a = Dense(TIME_STEPS, activation='softmax')(a)
	if SINGLE_ATTENTION_VECTOR:
		a = Lambda(lambda x: K.mean(x, axis=1), name='dim_reduction')(a)
		a = RepeatVector(input_dim)(a)
	a_probs = Permute((2, 1), name='attention_vec')(a)
	output_attention_mul = multiply([inputs, a_probs], name='attention_mul')
	return output_attention_mul


def model_attention_applied_after_lstm():
	inputs = Input(shape=(TIME_STEPS, INPUT_DIM,))
	lstm_units = 100
	lstm_out = LSTM(lstm_units, return_sequences=True)(inputs)
	attention_mul = attention_3d_block(lstm_out)
	attention_mul = Flatten()(attention_mul)
	output = Dense(nb_classes, activation='sigmoid')(attention_mul)
	model = Model(input=[inputs], output=output)
	return model


def model_attention_applied_before_lstm():
	inputs = Input(shape=(TIME_STEPS, INPUT_DIM,))
	attention_mul = attention_3d_block(inputs)
	lstm_units = 100
	attention_mul = LSTM(lstm_units, return_sequences=False)(attention_mul)
	output = Dense(nb_classes, activation='sigmoid')(attention_mul)
	model = Model(input=[inputs], output=output)
	return model


if __name__ == '__main__':

	N = 300000
	# N = 300 -> too few = no training
	inputs_1, outputs = X_train, Y_train

	if APPLY_ATTENTION_BEFORE_LSTM:
		m = model_attention_applied_before_lstm()
	else:
		m = model_attention_applied_after_lstm()

	m.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
	print(m.summary())

	m.fit([inputs_1], outputs, epochs=3, batch_size=64, validation_split=0.1)

	y_pred=m.predict(X_test, batch_size=batch_size)
	for i in range(len(y_pred)):
		print(y_pred[i], Y_test[i])
	# 	print(classification_report(Y_test, y_pred))
	# attention_vectors = []
	# for i in range(X_test.shape[0]):
	#     testing_inputs_1, testing_outputs = X_test[i], y_test[i]
	#     attention_vector = np.mean(get_activations(m,
	#                                                testing_inputs_1,
	#                                                print_shape_only=True,
	#                                                layer_name='attention_vec')[0], axis=2).squeeze()
	#     print('attention =', attention_vector)
	#     assert (np.sum(attention_vector) - 1.0) < 1e-5
	#     attention_vectors.append(attention_vector)

	# attention_vector_final = np.mean(np.array(attention_vectors), axis=0)
	# # plot part.
	# import matplotlib.pyplot as plt
	# import pandas as pd

	# pd.DataFrame(attention_vector_final, columns=['attention (%)']).plot(kind='bar',
	#                                                                      title='Attention Mechanism as '
	#                                                                            'a function of input'
	#                                                                            ' dimensions.')
	# plt.show()
