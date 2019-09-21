from testing import *
import numpy as np

folder = '/media/enigmaeth/My Passport/Datasets/linguistics data/eng_mand_equal'
x, y = make_class_array(folder)
print(x.shape, y.shape)
X_file = 'x_test_mfcc_' + (folder.split('/'))[-1]
Y_file = 'y_label_'+ (folder.split('/'))[-1]
np.save(X_file, x)  
np.save(Y_file, y)



# filename = "english1.wav"

# with open(filename, 'rb') as f:
#     print(read_in_audio(f))

# cd = make_class_array('/media/enigmaeth/My Passport/Datasets/Accent/clean_data')
# print(cd.shape)
# np.save('top_3_100_split_mfcc.npy', cd)  
# mf = make_mean_mfcc_df('/media/enigmaeth/My Passport/Datasets/Accent/sounds_wav')
# print(mf.shape)
# np.save('top_3_100_split_y.npy', mf)  
