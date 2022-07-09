# this file extracts SSIM and/or PSNR between distorted upscaled, low frame rate version and the pristine low frame version (pseudo-reference)
import os
import glob
import subprocess
from joblib import Parallel,delayed

distorted_yuv= glob.glob(os.path.join('/data/PV_VQA_Study/all_cut_upscaled_y4m_vids','*'))
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
    return str(fps)

def single_vid_ssim(i):
    dis_vid = distorted_yuv[i]
    content = os.path.basename(dis_vid).split('_')[0]
    fps = fps_from_content(content,'HFR')
    begin_time = dis_vid.split('_')[-1]
    dis_FR = os.path.basename(dis_vid).split('_')[2]
    dis_fps = fps_from_content(content,dis_FR)
    print(dis_fps,fps)
    if(dis_fps==fps):
        ref_video = os.path.join('/data/PV_VQA_Study/all_cut_upscaled_y4m_vids',content+'_SRC_SRC_SRC_SRC_'+begin_time[:-3]+'y4m')
    else:
        ref_video = os.path.join('/home/ubuntu/GREED/lbvfr/pseudo_reference_lbvfr/',content+'_SRC_SRC_SRC_SRC_'+begin_time[:-4]+'_pseudo_reference.y4m')

    height,width=str(3840),str(2160)
    msssim_outname = os.path.join('./msssim_features_PR/',os.path.splitext(os.path.basename(dis_vid))[0]+'.log')
    if(os.path.exists(msssim_outname)):
        return
    msssim_command = ' '.join(['/home/ubuntu/daala/tools/dump_msssim','-r','-y','-s',dis_vid,ref_video,'2>&1 >>',msssim_outname])
    print(msssim_command)
    #try:
    subprocess.check_call(msssim_command,shell=True)
#    subprocess.check_call(psnr_command)
    #except:
    #    return
    return

Parallel(n_jobs=80)(delayed(single_vid_ssim)(i) for i in range(len(distorted_yuv)))
#for i in range(len(distorted_yuv)):
#    single_vid_ssim(i)
