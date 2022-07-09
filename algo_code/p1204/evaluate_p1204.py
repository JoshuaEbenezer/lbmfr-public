import json
import glob
import os
import pandas as pd
from scipy.stats import spearmanr

dmos_df = pd.read_csv("/data/PV_VQA_Study/code/score_cleanup_code/lbvfr_dmos_from_mos.csv")
ground_truth = []
predictions = []

json_filenames = glob.glob(os.path.join("/home/ubuntu/bitstream_mode3_p1204_3/features/p1204_lbvfr_features","*.json"))
for json_file in json_filenames:
    video_name = os.path.splitext(os.path.basename(json_file))[0]
    if('SRC' in video_name):
        continue
    index = dmos_df.index[dmos_df["video"]==video_name].tolist() 
    dmos = dmos_df[dmos_df["video"]==video_name].dmos.iloc[0]
    ground_truth.append(dmos)

    with open(json_file) as open_file:
        data = json.load(open_file)
    predicted_score = data["per_sequence"]
    print(dmos,predicted_score)
    predictions.append(predicted_score)

srocc = spearmanr(predictions,ground_truth)
print(srocc)
    


#with open('path_to_file/person.json') as f:
#  data = json.load(f)
