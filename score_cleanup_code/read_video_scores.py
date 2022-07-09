import os
import numpy as np
from collections import defaultdict
import glob
import pandas as pd

filenames = glob.glob(os.path.join('./mos_sepsess_zscores/','*.csv'))
#print(filenames)

video_dict = defaultdict(list)
subject_dict=defaultdict(list)

for subject_csv in filenames:
    
    num = int(os.path.splitext(os.path.basename(subject_csv))[0].split('_')[1])
    
#    if(num<=30 or (num >=91 and num<=120)):
#    if((num>30 and num<=60) or (num >=121 and num<=150)):
#    print(num)
    if((num>60 and num<=90) or (num >=151 and num<=180)):
        print(num)
        subject_df = pd.read_csv(subject_csv)
        video_names = subject_df['video']
        for index,v in enumerate(video_names):
            score = subject_df['score'].iloc[index]
            vkey = os.path.splitext(v)[0]
            print(vkey,subject_csv)
            video_dict[vkey].append(score)
            subject_dict[vkey].append(str(num))



print(video_dict)
#print(len(video_dict))
scores = []
names = []
content = []
codec = []
fr = []
res = []
bitrate = [] 
subject_ids = []

for key,val in video_dict.items():
    print(key)
    print(len(val))
    #if(len(val)<20):
    #    continue
    subject_ids.append(subject_dict[vkey])
    scores.append(val)
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
score_df = pd.DataFrame(list(zip(names,scores,subject_ids,content,codec,fr,res,bitrate)),columns=['video','mos_list','subject_ids','content','codec','fr','res','bitrate'])
score_df.to_csv('./lbvfr_for_sureal_group3.csv')
#hfr_scores = []
#sfr_scores = []
#avc_scores = []
#hevc_scores = []
#
#res_4k_scores = []
#res_720p_scores = []
#res_540p_scores = []
#res_396p_scores = []
#res_288p_scores = []
#
#mean_score = dict()
#
#def res_fps_score(video_dict,res,fps):
#    res_fps_scores = []
#    for key,val in video_dict.items():
#        score = np.mean(val)
#        split_name = key.split('_')
#
#        if(split_name[-3]==res and split_name[-4]==fps):
#            res_fps_scores.append(score)
#    return res_fps_scores
#
#hfr_288p_score = res_fps_score(video_dict,'288p','HFR')
#hfr_396p_score = res_fps_score(video_dict,'396p','HFR')
#hfr_540p_score = res_fps_score(video_dict,'540p','HFR')
#hfr_720p_score = res_fps_score(video_dict,'720p','HFR')
#
#sfr_288p_score = res_fps_score(video_dict,'288p','SFR')
#sfr_396p_score = res_fps_score(video_dict,'396p','SFR')
#sfr_540p_score = res_fps_score(video_dict,'540p','SFR')
#sfr_720p_score = res_fps_score(video_dict,'720p','SFR')
#
#def disp(input_list):
#    print(np.mean(input_list))
#
#
#disp(hfr_288p_score)
#disp(hfr_396p_score)
#disp(hfr_540p_score)
#disp(hfr_720p_score)
#
#disp(sfr_288p_score)
#disp(sfr_396p_score)
#disp(sfr_540p_score)
#disp(sfr_720p_score)
