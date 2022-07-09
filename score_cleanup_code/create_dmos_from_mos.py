import os
import glob
import numpy as np
import pandas as pd

score_df = pd.read_csv('./lbvfr_sepsess_zscore_mos.csv')
copy_df = score_df.copy()
videos = list(score_df['video'])
print(np.min(score_df['mos']))
mos=score_df['mos']



raw_dmos = []

for index,vid in enumerate(videos):
    vid_content = vid.split('_')[0]
    if('SRC' in vid):
        copy_df.drop(index,inplace=True)
        print(len(copy_df))
        continue
    vid_time = vid.split('_')[-1]
    ref_vid = vid_content+'_SRC_SRC_SRC_SRC_'+vid_time
#    print(ref_vid)

    ref_score = score_df.iloc[videos.index(ref_vid)].mos
    vid_score = mos[index]
    raw_dmos.append(vid_score-ref_score)
copy_df['dmos'] = raw_dmos
copy_df.to_csv('./lbvfr_dmos_from_mos.csv')
