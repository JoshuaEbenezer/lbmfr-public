import pandas as pd
import subprocess
import numpy as np
import os
import glob
from joblib import Parallel,delayed

dis_metadata_csv = pd.read_csv("/data/PV_VQA_Study/code/lbvfr_distorted_metadata.csv")
print([i for i in dis_metadata_csv["original_video_name"]])

outfolder = './lbvfr_features'

def fps_from_content(content):
    if(content=='EPLDay' or content=='EPLNight' or content=='Cricket1' or content=='Cricket2' or content=='USOpen'):
        fps = 50
    elif(content=='TNFF' or content=='TNFNFL'):
        fps = 59.94
    return fps
def greed_single_vid(i):
    dis_basename = dis_metadata_csv['original_video_name'].iloc[i]
    dis_filename = os.path.join("/data/PV_VQA_Study/all_cut_upscaled_y4m_vids",dis_basename)
    print(dis_filename)

    dis_fps = str(dis_metadata_csv['fps'].iloc[i])

    content = dis_metadata_csv['content'].iloc[i]
    begin_time = dis_metadata_csv['begin_time'].iloc[i]
    orig_basename = content+'_SRC_SRC_SRC_SRC_'+str(begin_time)+'.y4m'
     # for LIVE ETRI, the distorted version's FPS was made to match the original by interpolation
#    dis_fps = orig_fps
    orig_filename = os.path.join("/data/PV_VQA_Study/all_cut_upscaled_y4m_vids/",orig_basename)
    orig_fps = str(fps_from_content(content))
    print(orig_filename,orig_fps)
    outname = os.path.join(outfolder,os.path.splitext(os.path.basename(dis_filename))[0]+'.z')
    if(os.path.exists(outname)):
        return
    if not (os.path.exists(orig_filename)):
        print(orig_filename, ' does not exist')
    if not (os.path.exists(dis_filename)):
        print(dis_filename,' does not exist')
    subprocess.check_call(['./run_greed.sh',orig_filename,dis_filename,orig_fps,dis_fps,str(2160),str(3840),str(8),outfolder])
#Parallel(n_jobs=40)(delayed(greed_single_vid)(i) for i in range(len(dis_metadata_csv)))
for i in range(len(dis_metadata_csv)):
    greed_single_vid(i)
