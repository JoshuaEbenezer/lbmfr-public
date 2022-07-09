import os
import glob
import subprocess
from joblib import Parallel,delayed

distorted_yuv= glob.glob(os.path.join('/data/PV_VQA_Study/all_cut_upscaled_hfr_yuv_vids/','*'))

def single_vid_vmaf(i):
    dis_vid = distorted_yuv[i]
    content = os.path.basename(dis_vid).split('_')[0]
    fr = os.path.basename(dis_vid).split('_')[2]
    begin_time = dis_vid.split('_')[-1]
    ref_video = os.path.join('/data/PV_VQA_Study/all_cut_upscaled_yuv_vids',content+'_SRC_SRC_SRC_SRC_'+begin_time[:-3]+'yuv')

    height,width=str(3840),str(2160)
    outname = os.path.join('./vmaf_features_dup/',os.path.splitext(os.path.basename(dis_vid))[0]+'.json')
    if(os.path.exists(outname)):
        return
    command = ['./run_vmaf.sh',ref_video,dis_vid,outname]
    print(' '.join(command))
    try:
        subprocess.check_call(command)
    except:
        return
    return

Parallel(n_jobs=10)(delayed(single_vid_vmaf)(i) for i in range(len(distorted_yuv)))
#for i in range(len(distorted_yuv)):
#    single_vid_vmaf(i)
