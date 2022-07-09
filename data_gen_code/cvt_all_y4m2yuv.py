import pandas as pd
from joblib import Parallel,delayed
import subprocess
import os
import glob



filenames = glob.glob(os.path.join('/data/PV_VQA_Study/all_cut_upscaled_hfr_motioninterpolated_yuv_vids/','*'))
print(filenames)
def run_ffmpeg(filenames,i):
    input_vid = filenames[i]
    out_mp4_vid = os.path.join('/data/PV_VQA_Study/all_cut_upscaled_hfr_motioninterpolated_y4m_vids',os.path.splitext(os.path.basename(input_vid))[0]+'.y4m')
    if(os.path.exists(out_mp4_vid)):
        return
    command = ['./cvt2y4m.sh',input_vid,out_mp4_vid,fps,w,h]
    print(command)
    os.system(' '.join(command))
    return


Parallel(n_jobs=32)(delayed(run_ffmpeg)(filenames,i) for i in range(len(filenames)))
#for i in range(len(filenames)):
#    run_ffmpeg(filenames,i)
