import numpy as np
from joblib import dump
from sklearn.preprocessing import OneHotEncoder
import os
import glob
import pandas as pd

sureal_csv = pd.read_csv('../../../HFR/variable_length_chipqa/ETRI_metadata.csv')

video_names = sureal_csv['video']
qp = np.expand_dims(sureal_csv['qp'],1)
fr = sureal_csv['fps']
resolution = sureal_csv['resolution']
bitrate = np.expand_dims(sureal_csv['bitrate'],1)

fr_onehot = np.asarray(OneHotEncoder().fit_transform(np.expand_dims(fr, axis=1)).toarray())
resolution_onehot = np.asarray(OneHotEncoder().fit_transform(np.expand_dims(resolution, axis=1)).toarray())
print(resolution_onehot)
#print(bitrate)

metadata_features = np.concatenate((qp, fr_onehot, resolution_onehot, bitrate), axis=1)
X  = {'features': metadata_features,'video':video_names}
dump(X, './etri_metadata_floatonehot_features.joblib')
print(metadata_features.shape)









