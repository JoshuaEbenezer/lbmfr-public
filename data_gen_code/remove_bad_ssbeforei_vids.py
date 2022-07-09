import os
import glob

filenames1 = glob.glob(os.path.join('/data/PV_VQA_Study/all_cut_vids_ss_before_i','*'))
filenames2 = glob.glob(os.path.join('/data/PV_VQA_Study/all_cut_vids_ss_after_i','*'))
base_filename2 = [os.path.basename(f2) for f2 in filenames2]

for f1 in filenames1:
    base = os.path.basename(f1)
    if(base in base_filename2):
        print(base, ' has to go')
        os.remove(f1)
    


