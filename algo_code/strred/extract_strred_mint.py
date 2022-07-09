import numpy as np
import os
import glob
import subprocess
from joblib import Parallel,delayed,dump
import scipy.ndimage
import scipy.linalg
from strred_utils import *


def est_params(frame, blk, sigma_nn):
    h, w = frame.shape
    sizeim = np.floor(np.array(frame.shape)/blk) * blk
    sizeim = sizeim.astype(int)

    frame = frame[:sizeim[0], :sizeim[1]]

    #paired_products
    temp = []
    for u in range(blk):
      for v in range(blk):
        temp.append(np.ravel(frame[v:(sizeim[0]-(blk-v)+1), u:(sizeim[1]-(blk-u)+1)]))
    temp = np.array(temp).astype(np.float32)

    cov_mat = np.cov(temp, bias=1).astype(np.float32)

    # force PSD
    eigval, eigvec = np.linalg.eig(cov_mat)
    Q = np.matrix(eigvec)
    xdiag = np.matrix(np.diag(np.maximum(eigval, 0)))
    cov_mat = Q*xdiag*Q.T

    temp = []
    for u in range(blk):
      for v in range(blk):
        temp.append(np.ravel(frame[v::blk, u::blk]))
    temp = np.array(temp).astype(np.float32)

    # float32 vs float64 difference between python2 and python3
    # avoiding this problem with quick cast to float64
    V,d = scipy.linalg.eigh(cov_mat.astype(np.float64))
    V = V.astype(np.float32)

    # Estimate local variance
    sizeim_reduced = (sizeim/blk).astype(int)
    ss = np.zeros((sizeim_reduced[0], sizeim_reduced[1]), dtype=np.float32)
    if np.max(V) > 0:
      # avoid the matrix inverse for extra speed/accuracy
      ss = scipy.linalg.solve(cov_mat, temp)
      ss = np.sum(np.multiply(ss, temp) / (blk**2), axis=0)
      ss = ss.reshape(sizeim_reduced)

    V = V[V>0]

    # Compute entropy
    ent = np.zeros_like(ss, dtype=np.float32)
    for u in range(V.shape[0]):
      ent += np.log2(ss * V[u] + sigma_nn) + np.log(2*np.pi*np.exp(1))


    return ss, ent


def extract_info(frame1, frame2):
    blk = 3
    sigma_nsq = 0.1
    sigma_nsqt = 0.1

    model = SpatialSteerablePyramid(height=6)
    y1 = model.extractSingleBand(frame1, filtfile="sp5Filters", band=0, level=4)
    y2 = model.extractSingleBand(frame2, filtfile="sp5Filters", band=0, level=4)

    ydiff = y1 - y2

    ss, q = est_params(y1, blk, sigma_nsq)
    ssdiff, qdiff = est_params(ydiff, blk, sigma_nsqt)


    spatial = np.multiply(q, np.log2(1 + ss))
    temporal = np.multiply(qdiff, np.multiply(np.log2(1 + ss), np.log2(1 + ssdiff)))

    return spatial, temporal
def compute_strred(referenceVideoData, distortedVideoData):
    """Computes Spatio-Temporal Reduced Reference Entropic Differencing (ST-RRED) Index. [#f1]_

    Both video inputs are compared over frame differences, with quality determined by
    differences in the entropy per subband.

    Parameters
    ----------
    referenceVideoData : ndarray
        Reference video, ndarray of dimension (T, M, N, C), (T, M, N), (M, N, C), or (M, N),
        where T is the number of frames, M is the height, N is width,
        and C is number of channels. Here C is only allowed to be 1.

    distortedVideoData : ndarray
        Distorted video, ndarray of dimension (T, M, N, C), (T, M, N), (M, N, C), or (M, N),
        where T is the number of frames, M is the height, N is width,
        and C is number of channels. Here C is only allowed to be 1.

    Returns
    -------
    strred_array : ndarray
        The ST-RRED results, ndarray of dimension ((T-1)/2, 4), where T
        is the number of frames.  Each row holds spatial score, temporal score,
        reduced reference spatial score, and reduced reference temporal score.

    strred : float
        The final ST-RRED score if all blocks are averaged after comparing
        reference and distorted data. This is close to full-reference.

    strredssn : float
        The final ST-RRED score if all blocks are averaged before comparing
        reference and distorted data. This is the reduced reference score.

    References
    ----------

    .. [#f1] R. Soundararajan and A. C. Bovik, "Video Quality Assessment by Reduced Reference Spatio-temporal Entropic Differencing," IEEE Transactions on Circuits and Systems for Video Technology, April 2013.

    """


    assert(referenceVideoData.shape == distortedVideoData.shape)

    T, M, N, C = referenceVideoData.shape

    assert C == 1, "strred called with videos containing %d channels. Please supply only the luminance channel" % (C,)

    referenceVideoData = referenceVideoData[:, :, :, 0]
    distortedVideoData = distortedVideoData[:, :, :, 0]

    rreds = []
    rredt = []

    rredssn = []
    rredtsn = []

    for i in range(0, T-1, 2):
      refFrame1 = referenceVideoData[i].astype(np.float32)
      refFrame2 = referenceVideoData[i+1].astype(np.float32)

      disFrame1 = distortedVideoData[i].astype(np.float32)
      disFrame2 = distortedVideoData[i+1].astype(np.float32)

      spatialRef, temporalRef = extract_info(refFrame1, refFrame2)
      spatialDis, temporalDis = extract_info(disFrame1, disFrame2)

      rreds.append(np.mean(np.abs(spatialRef - spatialDis)))
      rredt.append(np.mean(np.abs(temporalRef - temporalDis)))


    rreds = np.array(rreds)
    rredt = np.array(rredt)

    srred = np.mean(rreds)
    trred = np.mean(rredt)
    strred = srred * trred

    return strred
def fread(fid, nelements, dtype):
     if dtype is str:
         dt = np.uint8  # WARNING: assuming 8-bit ASCII for np.str!
     else:
         dt = dtype

     data_array = np.fromfile(fid, dt, nelements)
     data_array.shape = (nelements, 1)

     return data_array

def y4mFileRead(file1,width, height,startFrame):
#    """Cut the YUV file at startFrame position for numFrame frames"""
    oneFrameNumBytes = int(width*height*1.5)

        # header info
    line1 = file1.readline()

    # string of FRAME 
    line2 = file1.readline()

    frameByteOffset = len(line1)+(len(line2)+oneFrameNumBytes) * startFrame

    # each frame begins with the 5 bytes 'FRAME' followed by some zero or more characters"
    bytesToRead = oneFrameNumBytes + len(line2)

    file1.seek(frameByteOffset)
    y1 = fread(file1,height*width,np.uint8)
    y = np.reshape(y1,(height,width,1))
    return y
def yuv_read(file_object,width,height,frame_num):
    file_object.seek(int(frame_num*height*width*1.5))
    y1 = fread(file_object,height*width,np.uint8)
    y = np.reshape(y1,(height,width,1))
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

def single_vid_strred(i):
    dis_vid = distorted_yuv[i]
    content = os.path.basename(dis_vid).split('_')[0]
    fps = fps_from_content(content,'HFR')
    begin_time = dis_vid.split('_')[-1]
    dis_FR = os.path.basename(dis_vid).split('_')[2]
    dis_fps = fps_from_content(content,dis_FR)
    print(dis_fps,fps)
    if(dis_fps==fps):
        print('same fps, already computed, exiting')
        return
    else:
        ref_video = os.path.join('/data/PV_VQA_Study/all_cut_upscaled_y4m_vids',content+'_SRC_SRC_SRC_SRC_'+begin_time[:-4]+'.y4m')

    width,height=int(3840),int(2160)
    strred_outname = os.path.join('./strred_features_mint/',os.path.splitext(os.path.basename(dis_vid))[0]+'.z')
    if(os.path.exists(strred_outname)):
        return
    if('SFR' in vid_name):
        fr_file = os.path.join('./speed_features_mint',vid_name+'.z')
    else:
        fr_file = f
    print(ref_video,dis_vid,height,width,dis_fps,strred_outname)
    strred_list= []

    frame_num= 0 
    ref_vid_obj =  open(ref_video, 'r+b') 
    dis_vid_obj =  open(dis_vid, 'r+b') 
    while(True):

        try:
            ref_y = y4mFileRead(ref_vid_obj,width,height,frame_num)
            ref_y_next = y4mFileRead(ref_vid_obj,width,height,frame_num+1) 
            dis_y = yuv_read(dis_vid_obj,width,height,frame_num)
            dis_y_next = yuv_read(dis_vid_obj,width,height,frame_num+1)
        except Exception as e:
            print(e)
            print(frame_num, ' frames read')
            ref_vid_obj.close()
            dis_vid_obj.close()
            dump(strred_list,strred_outname)
            break
        ref_data = np.stack((ref_y,ref_y_next),axis=0)
        dis_data = np.stack((dis_y,dis_y_next),axis=0)
        strred = compute_strred(ref_data,dis_data)
        strred_list.append(strred)
        frame_num = frame_num+1



    #strred_command = ['./run_strred.sh',ref_video,dis_vid,strred_outname,dis_fps]
    #try:
    #subprocess.check_call(strred_command)
    #subprocess.check_call(psnr_command)
    #except:
    #    return
    return

Parallel(n_jobs=80)(delayed(single_vid_strred)(i) for i in range(len(distorted_yuv)))
#for i in range(len(distorted_yuv)):
#    single_vid_strred(i)
#single_vid_strred(0)
