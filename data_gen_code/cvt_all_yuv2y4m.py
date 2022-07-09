import pandas as pd
from joblib import Parallel,delayed
import subprocess
import os
import glob



filenames = glob.glob(os.path.join('/data/PV_VQA_Study/all_cut_upscaled_hfr_motioninterpolated_yuv_vids/','*'))
meta_csv = pd.read_csv('./lbvfr_distorted_metadata.csv')

print(filenames)
def fps_from_content(content,fr):
    if(content=='EPLDay' or content=='EPLNight' or content=='Cricket1' or content=='Cricket2' or content=='USOpen'):
        if(fr=='HFR'):
            fps = 50
        else:
            fps = 25
    elif(content=='TNFF' or content=='TNFNFL'):
        if(fr=='HFR'):
            fps = 59.94
        else:
            fps = 29.97
    return fps
def run_ffmpeg(filenames,i):
    input_vid = filenames[i]
    if('SRC' in input_vid or 'HFR' in input_vid):
        return
    y4m_vid = os.path.splitext(os.path.basename(input_vid))[0]+'.y4m'
    content = meta_csv[meta_csv['original_video_name']==y4m_vid].content.iloc[0]
    fps = str(fps_from_content(content,'HFR'))
    res = '3840x2160' 
    out_mp4_vid = os.path.join('/data/PV_VQA_Study/all_cut_upscaled_hfr_motioninterpolated_y4m_vids',os.path.splitext(os.path.basename(input_vid))[0]+'.y4m')
    if(os.path.exists(out_mp4_vid)):
        return
    command = ['./cvt2y4m.sh',input_vid,out_mp4_vid,fps,res]
    os.system(' '.join(command))
    return


Parallel(n_jobs=64)(delayed(run_ffmpeg)(filenames,i) for i in range(len(filenames)))
#for i in range(len(filenames)):
#    f = filenames[i]
#    run_ffmpeg(filenames,i)
