import os
import matplotlib.pyplot as plt
import numpy as np
import glob
import pandas as pd

hash_df = pd.read_csv('./hash_list.csv')
#print(hash_df)

hash_list = list(hash_df)
     
score_csv_list = glob.glob(os.path.join('./sep_sess_unique_scores/','*.csv'))
special_score = []
for score_csv in score_csv_list:
    dis_mos_zscores = []
    dis_vid = []
    raw_dmos = []
    ref_scores = []
    ref_videos = []
    orig_score_df = pd.read_csv(score_csv,header=0,names=['index','hash_name','score'])
    score_df= orig_score_df.drop('index',axis=1)
    scores = np.asarray(score_df['score'],dtype=np.float32) 
    mos_zscores = (scores-np.mean(scores))/np.std(scores)
    vid_name = [hash_df[hash_df['hash_video_name']==hash_name].original_video_name.iloc[0] for hash_name in score_df['hash_name']]
    print(vid_name)
    for index,vid in enumerate(vid_name):
        vid_content = vid.split('_')[0]
        vid_time = vid.split('_')[-1]
        ref_vid = vid_content+'_SRC_SRC_SRC_SRC_'+vid_time
        print(ref_vid)

        try:
            ref_score = score_df.iloc[vid_name.index(ref_vid)].score
        except:
            if('USOpen_SRC_SRC_SRC_SRC_176' in ref_vid):
                ref_score = 82
        vid_score = scores[index]
        if('SRC' not in vid):
            dis_vid.append(vid)
            raw_dmos.append(vid_score-ref_score)
            dis_mos_zscores.append(mos_zscores[index])
    
   
    dmos_score_df = pd.DataFrame(list(zip(dis_vid,raw_dmos)),columns=['video','raw_avg_dmos'])
#    score_df['zscores'] = zscores
#    score_df['original_video_name']=vid_name
    dmos_score_df.to_csv(os.path.join('./distorted_vids_dmos_rawavg',os.path.basename(score_csv)))
    print(len(dmos_score_df))
