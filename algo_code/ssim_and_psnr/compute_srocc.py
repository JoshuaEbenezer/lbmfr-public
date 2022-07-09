import numpy as np
import pandas as pd
import os
import glob
from scipy.stats import spearmanr,pearsonr
from scipy.optimize import curve_fit
import glob

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

filenames = glob.glob(os.path.join('./psnr_features_PR','*.log'))
score_df = pd.read_csv('/data/PV_VQA_Study/code/score_cleanup_code/lbvfr_dmos_from_raw_avg_mos.csv')


all_psnr = []
all_dmos = []
for infile in filenames:
    vid_name= os.path.splitext(os.path.basename(infile))[0]

    try:
        dmos = score_df[score_df['video']==vid_name].dmos.iloc[0]
    except:
        continue
    if('SFR' in vid_name):
        fr_file = os.path.join('./psnr_features_mint/',vid_name+'.log')
    else:
        fr_file = infile
    if(os.path.exists(fr_file)==False):
        continue
    psnr = []
    with open(fr_file) as f:
        line = f.readline()
        print(line)
        print([l for l in line])
        if(len(line)<5):
            print(fr_file, ' is bad')
            os.remove(fr_file)
            continue
        y_psnr = float(line.split('Total:')[1][1:8])
        print(y_psnr)
        psnr.append(y_psnr)
    all_psnr.append(np.mean(psnr))
    all_dmos.append(dmos)

results(all_psnr,all_dmos)



