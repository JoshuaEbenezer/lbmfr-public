import numpy as np
import pandas as pd
import os
from joblib import load,dump
from scipy.stats import spearmanr,pearsonr
from scipy.optimize import curve_fit
import glob

filenames = glob.glob('./lbvfr_features/*.z')
all_sgreed = []
all_tgreed = []
all_dmos = []
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

for f in filenames:
    base = os.path.splitext(os.path.basename(f))[0]

    stgreed_dict = load(f)
    print(stgreed_dict)
    stgreed = stgreed_dict['feature:']
    print(stgreed)
#    dmos = st
    print(stgreed.shape)
    sgreed = np.mean(stgreed[0]+stgreed[1])
    tgreed = np.mean(stgreed[2:])
    vid_name= os.path.splitext(os.path.basename(f))[0]
    print(vid_name,sgreed,tgreed)
    all_sgreed.append(sgreed)
    all_tgreed.append(tgreed)
    dmos = score_df[score_df['video']==vid_name].dmos.iloc[0]
    all_dmos.append(dmos)


results(all_sgreed,all_dmos)
results(all_tgreed,all_dmos)

