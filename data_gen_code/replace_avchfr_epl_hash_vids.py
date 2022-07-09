import pandas as pd
from shutil import copyfile
import os
import glob

filenames = glob.glob(os.path.join('../all_cut_y4m_vids','EPLDay_AVC_SFR_*'))
hash_df= pd.read_csv("./hash_list.csv")
print(hash_df)

for f in filenames:
    basename = os.path.basename(f)
    print(basename)
    hash_name = hash_df[hash_df['original_video_name']==basename].hash_video_name.iloc[0]
    print(hash_name)
    outhash_name = os.path.join('../avc_sfr_hash_vids',hash_name)
    copyfile(f,outhash_name)


