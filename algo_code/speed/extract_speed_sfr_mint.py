import numpy as np
import os
import glob
import cv2
from joblib import Parallel,delayed,dump
import scipy.ndimage
import skimage.util
import math

def gen_gauss_window(lw, sigma):
    sd = np.float32(sigma)
    lw = int(lw)
    weights = [0.0] * (2 * lw + 1)
    weights[lw] = 1.0
    sum = 1.0
    sd *= sd
    for ii in range(1, lw + 1):
        tmp = np.exp(-0.5 * np.float32(ii * ii) / sd)
        weights[lw + ii] = tmp
        weights[lw - ii] = tmp
        sum += 2.0 * tmp
    for ii in range(2 * lw + 1):
        weights[ii] /= sum
    return weights

def compute_speed(ref, ref_next, dis, dis_next, \
                             window):
    blk = 5;
    sigma_nsq = 0.1;
    times_to_down_size = 4; 

    #resize all frames
    for i in range(times_to_down_size):
        ref = np.array(cv2.resize(ref, None, fx=0.5, fy=0.5, \
                         interpolation=cv2.INTER_AREA),dtype=np.float32)
        ref_next = np.array(cv2.resize(ref_next, None, fx=0.5, fy=0.5, \
                              interpolation=cv2.INTER_AREA),dtype=np.float32)
        dis = np.array(cv2.resize(dis, None, fx=0.5, fy=0.5, \
                         interpolation=cv2.INTER_AREA),dtype=np.float32)
        dis_next = np.array(cv2.resize(dis_next, None, fx=0.5, fy=0.5, \
                              interpolation=cv2.INTER_AREA),dtype=np.float32)
    
    # calculate local averages    
    h, w = ref.shape
    mu_ref = np.zeros((h, w), dtype=np.float32)
    mu_dis = np.zeros((h, w), dtype=np.float32)
    
    scipy.ndimage.correlate1d(ref, window, 0, mu_ref, mode='reflect')
    scipy.ndimage.correlate1d(mu_ref, window, 1, mu_ref, mode='reflect')
    
    scipy.ndimage.correlate1d(dis, window, 0, mu_dis, mode='reflect')
    scipy.ndimage.correlate1d(mu_dis, window, 1, mu_dis, mode='reflect')
    
    # estimate local variances and conditional entropies in the spatial
    # domain for ith reference and distorted frames
    ss_ref, q_ref = est_params(ref - mu_ref, blk, sigma_nsq)
    spatial_ref = q_ref*np.log2(1+ss_ref)
    ss_dis, q_dis = est_params(dis - mu_dis, blk, sigma_nsq)
    spatial_dis = q_dis*np.log2(1+ss_dis)
    
    speed_s = np.nanmean(np.abs(spatial_ref.ravel() - spatial_dis.ravel()))
    speed_s_sn = np.abs(np.nanmean(spatial_ref.ravel() - spatial_dis.ravel()))
    
    ## frame differencing
    ref_diff = ref_next - ref;
    dis_diff = dis_next - dis;
    
    ## calculate local averages of frame differences
    mu_ref_diff = np.zeros((h, w), dtype=np.float32)
    mu_dis_diff = np.zeros((h, w), dtype=np.float32)
    
    scipy.ndimage.correlate1d(ref_diff, window, 0, mu_ref_diff, mode='reflect')
    scipy.ndimage.correlate1d(mu_ref_diff, window, 1, mu_ref_diff, mode='reflect')
    
    scipy.ndimage.correlate1d(dis_diff, window, 0, mu_dis_diff, mode='reflect')
    scipy.ndimage.correlate1d(mu_dis_diff, window, 1, mu_dis_diff, mode='reflect')
    
    """ Temporal SpEED
     estimate local variances and conditional entropies in the spatial
     domain for the reference and distorted frame differences """
     
    ss_ref_diff, q_ref = est_params(ref_diff - mu_ref_diff, blk, sigma_nsq)
    temporal_ref = q_ref*np.log2(1+ss_ref)*np.log2(1+ss_ref_diff)
    ss_dis_diff, q_dis = est_params(dis_diff - mu_dis_diff, blk, sigma_nsq)
    temporal_dis = q_dis*np.log2(1+ss_dis)*np.log2(1 + ss_dis_diff)
    
    speed_t = np.nanmean(np.abs(temporal_ref.ravel() - temporal_dis.ravel()));
    speed_t_sn = np.abs(np.nanmean(temporal_ref.ravel() - temporal_dis.ravel()));
    
    return speed_s, speed_s_sn, speed_t, speed_t_sn

def est_params(y, blk, sigma):
    """ 'ss' and 'ent' refer to the local variance parameter and the
        entropy at different locations of the subband
        y is a subband of the decomposition, 'blk' is the block size, 'sigma' is
        the neural noise variance """
    
    sizeim = np.floor(np.array(y.shape)/blk) * blk
    sizeim = sizeim.astype(np.int)
    y = y[:sizeim[0],:sizeim[1]].T
    
    temp = skimage.util.view_as_windows(np.ascontiguousarray(y), (blk,blk))\
    .reshape(-1,blk*blk).T
    
    cu = np.cov(temp, bias=1).astype(np.float32)
    
    eigval, eigvec = np.linalg.eig(cu)
    Q = np.matrix(eigvec)
    #L = diag(diag(L).*(diag(L)>0))*sum(diag(L))/(sum(diag(L).*(diag(L)>0))+(sum(diag(L).*(diag(L)>0))==0));
    L = np.matrix(np.diag(np.maximum(eigval, 0)))
    
    cu = Q*L*Q.T
    temp = skimage.util.view_as_blocks(np.ascontiguousarray(y), (blk,blk))\
    .reshape(-1,blk*blk).T
    
    L,Q = np.linalg.eigh(cu.astype(np.float64))
    L = L.astype(np.float32)
    #Estimate local variance parameters
    if np.max(L) > 0:
        ss = scipy.linalg.solve(cu, temp)
        ss = np.sum(ss*temp, axis=0)/(blk*blk)
        ss = ss.reshape((int(sizeim[1]/blk), int(sizeim[0]/blk))).T
    else:
        ss = np.zeros((sizeim/blk).astype(np.int),dtype=np.float32)
    
    L = L[L>0]
    
    #Compute entropy
    ent = np.zeros_like(ss, dtype=np.float32)
    for u in range(len(L)):
        ent += np.log2(ss*L[u]+sigma) + np.log(2*math.pi*np.exp(1));
        
    return ss, ent

def fread(fid, nelements, dtype):
     if dtype is str:
         dt = np.uint8  # WARNING: assuming 8-bit ASCII for np.str!
     else:
         dt = dtype

     data_array = np.fromfile(fid, dt, nelements)
     data_array.shape = (nelements, 1)

     return data_array


def yuv_read(file_object,width,height,frame_num):
    file_object.seek(int(frame_num*height*width*1.5))
    y1 = fread(file_object,height*width,np.uint8)
    y = np.reshape(y1,(height,width))
    return y
distorted_yuv= glob.glob(os.path.join('/data/PV_VQA_Study/all_cut_upscaled_hfr_motioninterpolated_yuv_vids','*'))
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

def single_vid_speed(i):
    dis_vid = distorted_yuv[i]
    content = os.path.basename(dis_vid).split('_')[0]
    fps = fps_from_content(content,'HFR')
    begin_time = dis_vid.split('_')[-1]
    dis_FR = os.path.basename(dis_vid).split('_')[2]
    dis_fps = fps_from_content(content,dis_FR)
    print(dis_fps,fps)
    ref_video = os.path.join('/data/PV_VQA_Study/all_cut_upscaled_yuv_vids/',content+'_SRC_SRC_SRC_SRC_'+begin_time[:-3]+'yuv')

    width,height=int(3840),int(2160)
    speed_outname = os.path.join('./speed_features_mint/',os.path.splitext(os.path.basename(dis_vid))[0]+'.z')
#    if(os.path.exists(speed_outname)):
#        return
    print(ref_video,dis_vid,height,width,dis_fps,speed_outname)
    speed_list= []
    avg_window = gen_gauss_window(3, 7.0/6.0)

    frame_num= int(0) 
    while(True):
        ref_video_obj = open(ref_video,'r+b')
        dis_video_obj = open(dis_vid,'r+b')
        try:
            ref_y = yuv_read(ref_video_obj,width,height,frame_num)
            ref_y_next = yuv_read(ref_video_obj,width,height,frame_num+1) 
            dis_y = yuv_read(dis_video_obj,width,height,frame_num)
            dis_y_next = yuv_read(dis_video_obj,width,height,frame_num+1)
        except:
            print(frame_num, ' frames read')
            ref_video_obj.close()
            dis_video_obj.close()
            dump(speed_list,speed_outname)
            break
        speed = compute_speed(ref_y,ref_y_next,dis_y,dis_y_next,avg_window)
        print(speed)
        speed_list.append(speed)
        frame_num = frame_num+1



    #speed_command = ['./run_speed.sh',ref_video,dis_vid,speed_outname,dis_fps]
    #try:
    #subprocess.check_call(speed_command)
    #subprocess.check_call(psnr_command)
    #except:
    #    return
    return

Parallel(n_jobs=80)(delayed(single_vid_speed)(i) for i in range(len(distorted_yuv)))
#single_vid_speed(0)
