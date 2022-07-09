import os
import matplotlib.pyplot as plt
import numpy as np
import glob
import pandas as pd

hash_df = pd.read_csv('./hash_list.csv')
#print(hash_df)

hash_list = list(hash_df)

# certain subjects had both their sessions before the videos were corrected
group1_subject_ids= np.concatenate((np.arange(1,31),np.arange(91,96))) 


group2_bad_avc_sfr_subject_ids = [32,35,36,37,40]
group2_bad_avc_sfr_subject_ids_firstsess = [34,38,39,41]
     
score_csv_list = glob.glob(os.path.join('./sep_sess_unique_scores/','*.csv'))
for score_csv in score_csv_list:
    print(score_csv)
    subject_num = int(os.path.splitext(os.path.basename(score_csv))[0].split('_')[1])
    print(subject_num)
    orig_score_df = pd.read_csv(score_csv,header=0)#names=['index','hash_name','score'])
    score_df= orig_score_df.drop('index',axis=1)
    scores = np.asarray(score_df['score'],dtype=np.float32) 
    first_session = list(score_df['first_session'])
    vid_name = [hash_df[hash_df['hash_video_name']==hash_name].original_video_name.iloc[0] for hash_name in score_df['hash_name']]
    score_df['video']=vid_name
    if(subject_num in [1,4,7,8]):
        print('ok')
        score_df= score_df[~(score_df['video'].str.contains('EPLDay') & score_df['video'].str.contains('AVC') \
                & score_df['video'].str.contains('HFR') & ~score_df['video'].str.contains('540p'))]
    elif(subject_num in [2,3,5,6]):
        score_df = score_df[~(score_df['video'].str.contains('EPLDay') & (score_df['first_session']==True) \
                &  score_df['video'].str.contains('AVC') & score_df['video'].str.contains('HFR') &  ~score_df['video'].str.contains('540p'))]
    if(subject_num in group1_subject_ids or subject_num in group2_bad_avc_sfr_subject_ids):
        score_df= score_df[~(score_df['video'].str.contains('EPLDay') & score_df['video'].str.contains('AVC') \
                & score_df['video'].str.contains('SFR') & ~score_df['video'].str.contains('540p'))]
    elif(subject_num in group2_bad_avc_sfr_subject_ids_firstsess):
        score_df = score_df[~(score_df['video'].str.contains('EPLDay') & (score_df['first_session']==True) \
                &  score_df['video'].str.contains('AVC') & score_df['video'].str.contains('SFR') &  ~score_df['video'].str.contains('540p'))]
    first_sess_scores = [scores[i] for i in range(len(score_df)) if (first_session[i]==True)]
    second_sess_scores = [scores[i] for i in range(len(score_df)) if (first_session[i]!=True) ]
    first_sess_zscores = (first_sess_scores-np.mean(first_sess_scores))/np.std(first_sess_scores)
    second_sess_zscores = (second_sess_scores-np.mean(second_sess_scores))/np.std(second_sess_scores)
    zscores = 100*(np.concatenate((first_sess_zscores,second_sess_zscores))+3)/6
    score_df['raw_mos_zscore'] = zscores

    score_df.to_csv(os.path.join('./mos_sepsess_zscores',os.path.basename(score_csv)))
    print(len(score_df))
