import os
from scipy.optimize import curve_fit
from scipy.stats import pearsonr,spearmanr
import numpy as np
import glob
import pandas as pd
import json

filenames = glob.glob(os.path.join('./vmaf_features_PR','*.json'))
score_df = pd.read_csv('/data/PV_VQA_Study/code/score_cleanup_code/lbvfr_dmos_from_mos.csv')

def results(all_preds,all_dmos):
    all_preds = np.asarray(all_preds)
    print(np.max(all_preds),np.min(all_preds))
    all_preds[np.isnan(all_preds)]=0
    all_dmos = np.asarray(all_dmos)
    [[b0, b1, b2, b3, b4], _] = curve_fit(lambda t, b0, b1, b2, b3, b4: b0 * (0.5 - 1.0/(1 + np.exp(b1*(t - b2))) + b3 * t + b4),
                                          all_preds, all_dmos, p0=0.5*np.ones((5,)), maxfev=20000)

    preds_fitted = b0 * (0.5 - 1.0/(1 + np.exp(b1*(all_preds - b2))) + b3 * all_preds+ b4)
    preds_srocc = spearmanr(preds_fitted,all_dmos)
    preds_lcc = pearsonr(preds_fitted,all_dmos)
    preds_rmse = np.sqrt(np.mean(preds_fitted-all_dmos)**2)
    print('SROCC:')
    print(preds_srocc[0])
    print('LCC:')
    print(preds_lcc[0])
    print('RMSE:')
    print(preds_rmse)
    print(len(all_preds),' videos were read')

all_vmaf = []
all_dmos = []
for infile in filenames:
    if('SRC' in infile):
        continue
    vid= os.path.splitext(os.path.basename(infile))[0]
    try:
        dmos = score_df[score_df['video']==vid].dmos.iloc[0]
    except:
        continue
    if('SFR' in vid):
        infile = os.path.join('./vmaf_features_mint',vid+'.json')

    vmaf = []
    with open(infile) as f:
        try:
            flines = json.load(f)
        except Exception as e:
            print(e)
            continue
    pooled_metrics = flines['pooled_metrics']
    y_vmaf = pooled_metrics['vmaf']['mean']

    all_vmaf.append(y_vmaf)
    print(vid)
    all_dmos.append(dmos)

results(all_vmaf,all_dmos)


