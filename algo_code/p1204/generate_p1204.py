import json
from joblib import Parallel,delayed
import glob
import os
import subprocess

os.chdir('/home/ubuntu/bitstream_mode3_p1204_3')
filenames = ['/data/PV_VQA_Study/problematic_all_cut_vids_ss_before_i/TNFF_AVC_HFR_288p_300K_144.mp4'] # glob.glob(os.path.join('/data/PV_VQA_Study/all_cut_vids_ss_after_i','*'))
results_folder = './' #'/home/ubuntu/bitstream_mode3_p1204_3/features/p1204_lbvfr_features'
def generate_p1204_scores(filenames,i):
    file = filenames[i]
    basename = os.path.splitext(os.path.basename(file))[0]+'.json'
    print(basename)
    output_name = os.path.join(results_folder,basename)
    if(os.path.exists(output_name)==True):
        print('File already exists')
        return
    if('TNFF_SRC' in basename or 'Cricket' in basename):
        print('TNF_SRC')
        return
    print('Generating')
    #try:
    #    p = subprocess.Popen(['/home/ubuntu/bitstream_mode3_p1204_3/run_p1204.sh',file, results_folder])
    #    p.wait()
    #except:
    #    return
    subprocess.check_call(['/home/ubuntu/bitstream_mode3_p1204_3/run_p1204.sh',file, results_folder])
    #p = subprocess.Popen(['/home/ubuntu/bitstream_mode3_p1204_3/run_p1204.sh',file, results_folder])
    #p.wait()
    return

for i in range(len(filenames)):
    generate_p1204_scores(filenames,i) 
#Parallel(n_jobs=-1)(delayed(generate_p1204_scores)(filenames,i) for i in range(len(filenames)))
