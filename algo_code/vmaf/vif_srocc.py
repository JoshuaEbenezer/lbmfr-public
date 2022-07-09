import os
import glob
import pandas as pd
import json
from scipy.stats import spearmanr

filenames = glob.glob(os.path.join('./vmaf_features','*.json'))
score_df = pd.read_csv('/data/PV_VQA_Study/code/score_cleanup_code/lbvfr_dmos_from_mos.csv')


all_vif = []
all_dmos = []
for infile in filenames:
    vid_name= os.path.splitext(os.path.basename(infile))[0]

    vif = []
    with open(infile) as f:
        flines = json.load(f)
    pooled_metrics = flines['pooled_metrics']
    y_vif = pooled_metrics['integer_vif_scale0']['mean']

    print(y_vif)
    all_vif.append(y_vif)
    dmos = score_df[score_df['video']==vid_name].dmos.iloc[0]
    all_dmos.append(dmos)

srocc = spearmanr(all_vif,all_dmos)
print(srocc[0])
print(len(all_vif),' videos were read')


