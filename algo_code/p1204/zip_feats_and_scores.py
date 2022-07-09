import json
import numpy as np
from joblib import dump,Parallel,delayed
import glob
import os
import subprocess
import pandas as pd

#os.chdir('/home/ubuntu/bitstream_mode3_p1204_3')
results_folder = './p1204_lbvfr_features'
filenames = glob.glob(os.path.join('/home/ubuntu/bitstream_mode3_p1204_3/features/p1204_lbvfr_features/','*.json'))

dmos_df = pd.read_csv("../../score_cleanup_code/lbvfr_dmos_from_mos.csv")
ground_truth = []
feature_list = []
names = []

def zip_feats_and_scores(filenames):
    for i in range(len(filenames)):
        json_file = filenames[i]
        video_name = os.path.splitext(os.path.basename(json_file))[0]
        if('SRC' in video_name):
            continue
        print(video_name)
        names.append(video_name)
        dmos = dmos_df[dmos_df["video"]==video_name].dmos.iloc[0]
        ground_truth.append(dmos)

        with open(json_file) as open_file:
            data = json.load(open_file)
            feats = np.asarray([val for key,val in data['features'].items() if(key!="predicted_mos_mode3_baseline")])
            print(data['features'])
            print(feats)
            out_dict = {'features':feats,'names':video_name,'scores':dmos}
            out_name = video_name+'.z' 
            dump(out_dict,os.path.join(results_folder,out_name))
    return


zip_feats_and_scores(filenames)
