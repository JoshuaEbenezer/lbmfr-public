# this file reads all the subjects' raw DMOS zscores and averages them to create a video level score

import os
import numpy as np
from collections import defaultdict
import glob
import pandas as pd

filenames = glob.glob(os.path.join('./mos_sepsess_zscores','*.csv'))

video_dict = defaultdict(list)

for subject_csv in filenames:
    subject_df = pd.read_csv(subject_csv)
    video_names = subject_df['video']
    for index,v in enumerate(video_names):
        score = subject_df['raw_mos_zscore'].iloc[index]
        vkey = os.path.splitext(v)[0]
        print(vkey,subject_csv)
        video_dict[vkey].append(score)



print(video_dict)
print(len(video_dict))
scores = []
names = []
content = []
codec = []
fr = []
res = []
bitrate = [] 
std_devs = []

for key,val in video_dict.items():
    print(key)
    print(len(val))
    #if(len(val)<20):
    #    continue
    scores.append(np.mean(val))
    std_devs.append(np.std(val))
    names.append(key)
    split_name = key.split('_')
    content.append(split_name[0]+'_'+split_name[-1])
    codec.append(split_name[1])
    fr.append(split_name[2])
    res.append(split_name[3])
    if(split_name[4]=='SRC'):
        bitrate.append(100000)
    else:
        bitrate.append(split_name[4][:-1])
print([b for b in bitrate])
score_df = pd.DataFrame(list(zip(names,scores,std_devs,content,codec,fr,res,bitrate)),columns=['video','mos','mos_std','content','codec','fr','res','bitrate'])
score_df.to_csv('./lbvfr_sepsess_zscore_mos.csv')
