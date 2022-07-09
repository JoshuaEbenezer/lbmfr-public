import numpy as np
from joblib import dump,load
import pandas as pd
import os
import glob
from scipy.stats import spearmanr,pearsonr
from scipy.optimize import curve_fit

filenames = glob.glob(os.path.join('./old_psnr_ssim/psnr_features','*.log'))
score_df = pd.read_csv('/data/PV_VQA_Study/code/score_cleanup_code/lbvfr_dmos_from_raw_avg_mos.csv')

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

all_psnr = []
all_dmos = []
for infile in filenames:
    vid_name= os.path.splitext(os.path.basename(infile))[0]
    outname = os.path.join('./old_psnr_ssim/psnr_features_avg',vid_name+'.z')
    if(os.path.exists(outname)==True):
        print('already stored ', vid_name,'. Loading')
        all_psnr.append(load(outname))
        dmos = score_df[score_df['video']==vid_name].dmos.iloc[0]
        all_dmos.append(dmos)
        continue

    psnr = []
    with open(infile) as f:
        f = f.readlines()
    print(infile,len(f))
    if(len(f)<100):
        print(infile,' was not included')
        continue
    for line in f:
        try:
            y_psnr = float(line.split('psnr_y:')[1][0:5])
        except:
            continue
        print(y_psnr)
        psnr.append(y_psnr)
    dump(np.mean(psnr),outname)
    all_psnr.append(np.mean(psnr))
    dmos = score_df[score_df['video']==vid_name].dmos.iloc[0]
    all_dmos.append(dmos)





