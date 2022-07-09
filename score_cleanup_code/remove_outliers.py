import numpy as np
from collections import defaultdict
import cv2
import os
import glob
from scipy.stats import kurtosis
import pandas as pd



subj_csvs = glob.glob(os.path.join('./mos_sepsess_zscores/','*'))

video_dict = defaultdict(list)

for subject_csv in subj_csvs:
    subject_df = pd.read_csv(subject_csv)
    video_names = subject_df['video']
    for index,v in enumerate(video_names):
        score = 6*(subject_df['raw_mos_zscore'].iloc[index])/100 - 3
        vkey = os.path.splitext(v)[0]
#        print(vkey,subject_csv)
        video_dict[vkey].append(score)

gauss_list = np.zeros(len(video_dict),dtype=bool)
all_vids = []
video_score_list = []
video_std_list = []

for ii,key_val in enumerate(video_dict.items()):
    key = key_val[0]
    val = key_val[1]
    all_vids.append(key)
    kurt = kurtosis(val,fisher=False)
#    print(kurt)
    if(kurt>=2 and kurt<=4):
        gauss_list[ii] = True
    video_score_list.append(np.mean(val))
    video_std_list.append(np.std(val))
#print(gauss_list)
gauss_score_std_dict = dict((z[0],list(z[1:])) for z in zip(all_vids,gauss_list,video_score_list,video_std_list)) 
#print(video_std_list)


reject = np.zeros(len(video_dict),dtype=bool)
for jj,subject_csv in enumerate(subj_csvs):
    p = 0
    q = 0
    subject_df = pd.read_csv(subject_csv)
    video_names = subject_df['video']
    for index,v in enumerate(video_names):
        score = 6*(subject_df['raw_mos_zscore'].iloc[index])/100 - 3
        vkey = os.path.splitext(v)[0]
        #print(score,video_dict[vkey][1],video_dict[vkey][2])
        if(gauss_score_std_dict[vkey][0] == True): 
            if(score >= video_dict[vkey][1]+2*video_dict[vkey][2]):
                p = p+1
            elif(score <= video_dict[vkey][1]-2*video_dict[vkey][2]):
                q=q+1
        else:
            if(score >= video_dict[vkey][1]+np.sqrt(20)*video_dict[vkey][2]):
                p = p+1
            elif(score <= video_dict[vkey][1]-np.sqrt(20)*video_dict[vkey][2]):
                q=q+1
    if(p==0 and q==0):
        continue
    else:
        print((p+q)/len(subject_df))
        print(np.abs((p-q)/(p+q)))
        print('two conditions above')
        if(((p+q)/len(subject_df))>0.05 and np.abs((p-q)/(p+q))<0.3):
            reject[jj]=True
            print('rejected ', subject_csv)


 
