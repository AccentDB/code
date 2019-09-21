import numpy as np
from gen_y import generate_y
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report
from keras.models import load_model
from keras.utils import np_utils

nb_classes = 3

X_test = np.load('test_mfcc_merge_spanish_test.npy')
#print(X.shape)
# y = generate_y('/media/enigmaeth/My Passport/Datasets/Accent/sounds_wav')
#print(y.shape)

# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15)
""
# Y_train = np_utils.to_categorical(y_train, nb_classes)
# Y_test = np_utils.to_categorical(y_test, nb_classes)

#X_test = np.load('test_mfcc.npy')
print(X_test.shape)
y = np.array([2]*380)
#print(y)
Y_test = np_utils.to_categorical(y, nb_classes)
print(Y_test.shape)

model = load_model('model_20epochs.h5')
prediction = model.predict(X_test)
ct = 0
ans = []
for row in prediction:
	index = idx = 0
	ma = 0
	for col in row:
		if col > ma:
			idx = index
			ma = col
		index += 1
	#if ct == 10: break
	ct += 1
	ans.append(idx)

print(ans, len(ans))

score = model.evaluate(X_test, Y_test,  verbose=1)
print(score)