import pandas as pd
import sys
import subprocess
import os
import glob



#sys.stdout = open("framenos.txt", "w")

filenames = glob.glob(os.path.join('../../all_cut_vids_ss_before_i','*'))
def find_frames(input_vid):
    command = ['./check_framenos.sh',input_vid]
    proc = subprocess.check_output(command)
    output = proc.decode("utf-8")[:-1]
    return output
out_y4m = []
out_ss_after_i = []
vids = []

for input_vid in filenames:
    vid_name = os.path.splitext(os.path.basename(input_vid))[0]+'.y4m'
    vids.append(vid_name)
    y4m_vid = os.path.join('/data/PV_VQA_Study/all_cut_y4m_vids',vid_name)
    out_ss_after_i.append(find_frames(input_vid))
    out_y4m.append(find_frames(y4m_vid))
#sys.stdout.close()


df = pd.DataFrame(list(zip(vids,out_y4m,out_ss_after_i)))
df.to_csv('./ss_before_i_framenos.csv')

