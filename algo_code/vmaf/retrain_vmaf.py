import numpy as np
from scipy.optimize import curve_fit
import json
from joblib import Parallel,delayed
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from joblib import load
from scipy.stats import pearsonr,spearmanr
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV
import glob
import os


scores_df = pd.read_csv('/data/PV_VQA_Study/code/score_cleanup_code/lbvfr_dmos_from_raw_avg_mos.csv')
video_names = scores_df['video']
scores = scores_df['dmos']
#scores_df['content']=[ i[-9:] for i in scores_df['video'] ]
print(len(scores_df['content'].unique()))
srocc_list = []
test_zips = []

def find(lst, a):
    return [i for i, x in enumerate(lst) if x==a]
def results(all_preds,all_dmos):
    all_preds = np.asarray(all_preds)
    print(np.max(all_preds),np.min(all_preds))
    all_preds[np.isnan(all_preds)]=0
    all_dmos = np.asarray(all_dmos)
    #try:
    print(all_preds,all_dmos)
    try:
        [[b0, b1, b2, b3, b4], _] = curve_fit(lambda t, b0, b1, b2, b3, b4: b0 * (0.5 - 1.0/(1 + np.exp(b1*(t - b2))) + b3 * t + b4),
                         all_preds, all_dmos, p0=0.5*np.ones((5,)), maxfev=20000)
        preds_fitted = b0 * (0.5 - 1.0/(1 + np.exp(b1*(all_preds - b2))) + b3 * all_preds+ b4)
    except:
        preds_fitted = all_preds
    preds_srocc = spearmanr(preds_fitted,all_dmos)
    preds_lcc = pearsonr(preds_fitted,all_dmos)
    preds_rmse = np.sqrt(np.mean(preds_fitted-all_dmos)**2)
    print("SROCC:")
    print(preds_srocc[0])
    print("LCC:")
    print(preds_lcc[0])
    print("RMSE:")
    print(preds_rmse)
    print(len(all_preds),' videos were read')
    return preds_srocc[0],preds_lcc[0],preds_rmse

def single_run_svr(r):
    train,test = train_test_split(scores_df['content'].unique(),test_size=0.2,random_state=r)
    train_features = []
    train_indices = []
    test_features = []
    train_scores = []
    test_scores = []
    train_vids = []
    test_vids = []
    feature_folder= './vmaf_features_PR'

    for i,vid in enumerate(video_names):
        if('SRC' in vid):
            continue
        if('SFR' in vid):
            json_f = os.path.join('./vmaf_features_dup',vid+'.json')
        else:
            featfile_name = vid+'.json'
            json_f = os.path.join(feature_folder,featfile_name)
        score = scores[i]

        feature_list = []
        with open(json_f) as f:
            try:
                json_data = json.load(f)
            except Exception as e:
                continue
#            print(json_data)
            pool_metrics = json_data['pooled_metrics']
            for key in pool_metrics.keys():
                if(key=='vmaf'):
                    continue
                feature_list.append(pool_metrics[key]['mean'])
        feature = np.asarray(feature_list,dtype=np.float32)
        feature = np.nan_to_num(feature)
#        if(np.isnan(feature).any()):
#            print(vid)
        if(scores_df.loc[i]['content'] in train):
            train_features.append(feature)
            train_scores.append(score)
            train_indices.append(i)
            train_vids.append(vid)
            
        else:
            test_features.append(feature)
            test_scores.append(score)
            test_vids.append(vid)
    train_features = np.asarray(train_features)
    test_features = np.asarray(test_features)
#    naninds =np.argwhere(np.isnan(train_features)) 
#    nanshape = naninds.shape
#    for nanind in range(nanshape[0]):
#        actind = train_indices[nanind]
#        print(scores_df.loc[actind]['video'])
    scaler = StandardScaler()
    scaler.fit(train_features)
    X_train = scaler.transform(train_features)
    X_test = scaler.transform(test_features)
    grid_svr = GridSearchCV(SVR(),param_grid = {"gamma":np.logspace(-8,1,10),"C":np.logspace(1,10,10,base=2)},cv=5)
    grid_svr.fit(X_train, train_scores)
    preds =grid_svr.predict(X_test)
    srocc,lcc,rmse = results(preds,test_scores)
    return srocc,lcc,rmse

results_list = Parallel(n_jobs=-1)(delayed(single_run_svr)(r) for r in range(100))
#results_list = []
#for r in range(100):
#    results_list.append(single_run_svr(r))
print("median srocc is")
print(np.median([s[0] for s in results_list if s is not None ]))
print("median lcc is")
print(np.median([s[1] for s in results_list]))
print("median rmse is")
print(np.median([s[2] for s in results_list]))
print("std of srocc is")
print(np.std([s[0] for s in results_list]))
print("std of lcc is")
print(np.std([s[1] for s in results_list]))
print("std of rmse is")
print(np.std([s[2] for s in results_list]))


def unique_scores(test_zips):
    scores = []
    names =[]
    preds =[]
    for v in test_zips:
        print(v)
        for l in v:
            names.append(l[0])
            scores.append(l[1])
            preds.append(l[2])
    print(names)
    print(scores)

    nset = set(names)
    print(len(names))
    print(len(nset))
    print(nset)
    nscores = []
    npreds = []
    for n in nset:
        indices = find(names,n)
        nscores.append(np.mean([scores[i] for i in indices]))
        npreds.append(np.mean([preds[i] for i in indices]))
    print(nscores,npreds)

