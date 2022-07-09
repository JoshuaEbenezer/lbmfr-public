import numpy as np
from joblib import dump
from sklearn.preprocessing import OneHotEncoder
import os
import glob
import pandas as pd

sureal_csv = pd.read_csv('./lbvfr_for_sureal.csv')

video_names = sureal_csv['video']
content = [v.split('_')[0]+'_'+v.split('_')[-1] for v in video_names]
codec = np.asarray([v.split('_')[1] for v in video_names])
fr = [v.split('_')[2] for v in video_names]
resolution = [v.split('_')[3] for v in video_names]
bitrate = [v.split('_')[4] for v in video_names]

codec_onehot = OneHotEncoder().fit_transform(np.expand_dims(codec, axis=1)).toarray()
content_onehot = np.asarray(OneHotEncoder().fit_transform(np.expand_dims(content, axis=1)).toarray())
fr_onehot = np.asarray(OneHotEncoder().fit_transform(np.expand_dims(fr, axis=1)).toarray())
resolution_onehot = np.asarray(OneHotEncoder().fit_transform(np.expand_dims(resolution, axis=1)).toarray())
bitrate_onehot = np.asarray(OneHotEncoder().fit_transform(np.expand_dims(bitrate, axis=1)).toarray())
print(codec_onehot.shape)
print(codec_onehot)
print(resolution_onehot)
print(bitrate_onehot)
#print(bitrate)

metadata_features = np.concatenate((codec_onehot, fr_onehot, resolution_onehot, bitrate_onehot), axis=1)
X  = {'features': metadata_features,'video':video_names}
dump(X, './metadata_features.joblib')
print(metadata_features.shape)









