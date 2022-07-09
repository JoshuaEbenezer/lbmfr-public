# EPL Day AVC HFR encodes had a black border issue on July 12th. 

import numpy as np
import os 
from scipy.stats import spearmanr
import glob
import pandas as pd
from collections import defaultdict

# certain subjects had both their sessions before the videos were corrected
bb_subject_ids= np.concatenate((np.arange(1,10),[11,13],np.arange(16,22),[25,29,30]))#,32,35,36,37,40]))
#bb_subject_ids= [32,35,36,37,40]
# another group had only their first session before the videos were corrected, so we have to check if they actually saw the wrong videos
bb_first_sess_subject_ids = [14,22,23,24,26,27]#,34,38,39,41]
#bb_first_sess_subject_ids = [34,38,39,41]
other_subject_ids = np.delete(np.concatenate((np.arange(1,31),[91,92])),bb_subject_ids) #,121,122,125
#other_subject_ids = np.setdiff1d(np.concatenate((np.arange(31,61),[121,122,125])),np.concatenate((bb_subject_ids,bb_first_sess_subject_ids))) #,121,122,125

bb_csvs= ['./mos_sepsess_zscores_including_eplavc/score_'+str(n)+'.csv' for n in bb_subject_ids]
bb_first_sess_csvs= ['./mos_sepsess_zscores_including_eplavc/score_'+str(n)+'.csv' for n in bb_first_sess_subject_ids]
other_csvs= ['./mos_sepsess_zscores_including_eplavc/score_'+str(n)+'.csv' for n in other_subject_ids]

content = ['EPLDay','EPLNight','TNFF','TNFNFL','USOpen','Cricket1','Cricket2']

def aligned_list(d,ref_d):
    other_val = []
    for key,val in ref_d.items():
        other_val.append(d[key])
    return np.asarray(other_val),np.asarray(list(ref_d.values()))
def get_scores(bb_csvs,content,first_sess=False):
    ds = []
    for csv in bb_csvs:
        try:
            bb_df = pd.read_csv(csv)
        except:
            continue
        if(first_sess==True):
            epl_day_avc_hfr = bb_df[bb_df['video'].str.contains(content) & bb_df['video'].str.contains('AVC') & bb_df['video'].str.contains('SFR') & (bb_df['first_session']==True) & ~bb_df['video'].str.contains('540p')]
        else:
            epl_day_avc_hfr = bb_df[bb_df['video'].str.contains(content) & bb_df['video'].str.contains('AVC') & bb_df['video'].str.contains('SFR') & ~bb_df['video'].str.contains('540p')]
        vids = epl_day_avc_hfr['video']
        scores=epl_day_avc_hfr['raw_mos_zscore']
        #print(csv)
        print(epl_day_avc_hfr)
#        print(len(epl_day_avc_hfr))
        ds.append(dict(zip(vids,scores)))

    print(len(ds), ' in this group watched at least one of these videos')
    dd = defaultdict(list)
    for d in ds:
        for key,value in d.items():
            dd[key].append(value)


    score_dd = defaultdict(np.float32)
    for key,val in dd.items():
        score_dd[key] = np.mean(val)

    return score_dd

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
    for key,val in dd.items():
        score_dd[key] = np.mean(val)

    corrected_score_dd = get_scores(other_csvs,c)

    bad_list,corrected_list = aligned_list(score_dd,corrected_score_dd)
    print(c)
    print(spearmanr(bad_list,corrected_list))
    print(np.sqrt(np.mean(bad_list-corrected_list)**2))




