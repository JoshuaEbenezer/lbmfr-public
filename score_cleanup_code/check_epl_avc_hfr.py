# EPL Day AVC HFR encodes had a black border issue on July 12th. 
import matplotlib.pyplot as plt
import numpy as np
import os 
from scipy.stats import spearmanr
import glob
import pandas as pd
from collections import defaultdict

# certain subjects had both their sessions before the videos were corrected
bb_subject_ids= [1,4,7,8]
# another group had only their first session before the videos were corrected, so we have to check if they actually saw the wrong videos
bb_first_sess_subject_ids = [2,3,5,6]
other_subject_ids = np.setdiff1d(np.concatenate((np.arange(1,31),[91,92])),np.concatenate((bb_subject_ids,bb_first_sess_subject_ids)))

bb_csvs= ['./mos_sepsess_zscores_including_eplavc/score_'+str(n)+'.csv' for n in bb_subject_ids]
bb_first_sess_csvs= ['./mos_sepsess_zscores_including_eplavc/score_'+str(n)+'.csv' for n in bb_first_sess_subject_ids]
other_csvs= ['./mos_sepsess_zscores_including_eplavc/score_'+str(n)+'.csv' for n in other_subject_ids]

content = ['EPLDay','EPLNight','TNFF','TNFNFL','USOpen','Cricket1','Cricket2']

def get_scores(bb_csvs,content,first_sess=False):
    ds = []
    for csv in bb_csvs:
        try:
            bb_df = pd.read_csv(csv)
        except:
            continue
#        print(csv)
        if(first_sess==True):
            # (bb_df['first_session']==True)
            epl_day_avc_hfr =  bb_df[(bb_df['video'].str.contains(content) & (bb_df['first_session']==True) &  bb_df['video'].str.contains('AVC') & bb_df['video'].str.contains('HFR') &  ~bb_df['video'].str.contains('540p'))]
        else:
            epl_day_avc_hfr = bb_df[(bb_df['video'].str.contains(content) & bb_df['video'].str.contains('AVC') & bb_df['video'].str.contains('HFR') & ~bb_df['video'].str.contains('540p'))]
        vids = epl_day_avc_hfr['video']
        scores=epl_day_avc_hfr['raw_mos_zscore']
        #print(epl_day_avc_hfr)
#        print(len(epl_day_avc_hfr),' are the number of relevant videos watched')
        ds.append(dict(zip(vids,scores)))

#    print(len(ds), ' in this group watched the video')
    dd = defaultdict(list)
    for d in ds:
        for key,value in d.items():
            dd[key].append(value)


    score_dd = defaultdict(np.float32)
    for key,val in dd.items():
        score_dd[key] = np.mean(val)
#        print(key,score_dd[key])

#    print(len(score_dd), ' is the length of the dict from these subjects')
    return score_dd

def aligned_list(d,ref_d):
    other_val = []
    for key,val in ref_d.items():
        other_val.append(d[key])
    return np.asarray(other_val),np.asarray(list(ref_d.values()))



for c in content:
    bb_score_dd = get_scores(bb_csvs,c)
    bb_first_score_dd = get_scores(bb_first_sess_csvs,c,first_sess=True)
    dd = defaultdict(list)

    for d in (bb_score_dd,bb_first_score_dd):
        for key,value in d.items():
            try:
                dd[key].append(value)
            except:
                continue
    score_dd = defaultdict(np.float32)
    #print('Average scores for bad videos:')
    for key,val in dd.items():
        score_dd[key] = np.mean(val)
    corrected_score_dd = get_scores(other_csvs,c)
    bad_list,corrected_list = aligned_list(score_dd,corrected_score_dd)
    #plt.figure()
    #plt.scatter(corrected_list,bad_list)
    #plt.xlabel('MOS of other subjects')
    #plt.ylabel('MOS of subjects who watched bad encodes of EPLDay_AVC_HFR')
    #plt.title(c+'_AVC_HFR encodes (288p, 396p, 396p, 720p)')
    #plt.savefig('avc_hfr_scatter_plots/'+c+'.png')
    #plt.close()
    print(corrected_score_dd.keys(),bad_list,corrected_list)

    print(c)
    print(spearmanr(bad_list,corrected_list))
    print(np.sqrt(np.mean(bad_list-corrected_list)**2))




