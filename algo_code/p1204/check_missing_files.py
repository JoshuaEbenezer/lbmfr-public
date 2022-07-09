import os
import glob

folder1 = '/home/ubuntu/bitstream_mode3_p1204_3/features/p1204_lbvfr_features/*'
folder2 = '/data/PV_VQA_Study/all_cut_vids_ss_before_i/*'

filenames1 = [os.path.splitext(os.path.basename(f))[0] for f in glob.glob(folder1)]
filenames2 = [os.path.splitext(os.path.basename(f))[0] for f in glob.glob(folder2)]

diff = sorted(list(set(filenames2)-set(filenames1)))
for d in diff:
    print(d)
print(len(diff))
