import numpy as np
from joblib import dump
from sklearn.preprocessing import OneHotEncoder
import os
import glob
import pandas as pd

sureal_csv = pd.read_csv('ythfr_MOS.csv')

video_names = sureal_csv['video']
crf = np.expand_dims([v.split('_')[2] for v in video_names],1)
fr = np.expand_dims([v.split('_')[3].split('fps')[0] for v in video_names],1)


#fr_onehot = np.asarray(OneHotEncoder().fit_transform(np.expand_dims(fr, axis=1)).toarray())
#print(bitrate)

metadata_features = np.concatenate((crf,fr), axis=1)
X  = {'features': metadata_features,'video':video_names}
dump(X, './ythfr_metadata_float_features.joblib')
print(metadata_features.shape)









