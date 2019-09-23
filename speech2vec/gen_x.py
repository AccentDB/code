from mfcc import *
import numpy as np

folder = '../data/splits'

x = make_class_array(folder)
print(x.shape)
X_file = '../data/numpy_vectors/x_test_mfcc_' + (folder.split('/'))[-1]

print("saving  labels to ", X_file)
np.save(X_file, x)  



# filename = "english1.wav"

# with open(filename, 'rb') as f:
#     print(read_in_audio(f))

# cd = make_class_array('/media/enigmaeth/My Passport/Datasets/Accent/clean_data')
# print(cd.shape)
# np.save('top_3_100_split_mfcc.npy', cd)  
# mf = make_mean_mfcc_df('/media/enigmaeth/My Passport/Datasets/Accent/sounds_wav')
# print(mf.shape)
# np.save('top_3_100_split_y.npy', mf)  
