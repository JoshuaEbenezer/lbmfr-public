import pandas as pd
import subprocess
import os
import glob



filenames = glob.glob(os.path.join('../full_length_distorted_mp4_fullnames','EPLDay_AVC_SFR_*'))
print(filenames)
for input_vid in filenames:
    out_mp4_vid = os.path.join('../full_length_distorted_y4m',os.path.splitext(os.path.basename(input_vid))[0]+'.y4m')
#    if(os.path.exists(out_mp4_vid)):
#        continue
    command = ['./cvt2y4m.sh',input_vid,out_mp4_vid]
    print(command)
    subprocess.check_call(command)


