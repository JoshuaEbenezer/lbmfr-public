import os
import cv2
import glob


startFrame = 0
curFrameRate = 50
startTime = startFrame / curFrameRate
filePath = '../source_y4m/EPLNight_SRC_full_length.y4m'
file1 = open(filePath,'r+b')

import numpy as np

def fread(fid, nelements, dtype):
     if dtype is str:
         dt = np.uint8  # WARNING: assuming 8-bit ASCII for np.str!
     else:
         dt = dtype

     data_array = np.fromfile(fid, dt, nelements)
     data_array.shape = (nelements, 1)

     return data_array




def yuv_read(file_object,frame_num,height,width):
    y1 = fread(file_object,height*width,np.uint8)
    u1 = fread(file_object,height*width//4,np.uint8)
    v1 = fread(file_object,height*width//4,np.uint8)
    y = np.reshape(y1,(height,width))
    u = np.reshape(u1,(height//2,width//2)).repeat(2,axis=0).repeat(2,axis=1)
    v = np.reshape(v1,(height//2,width//2)).repeat(2,axis=0).repeat(2,axis=1)
    return y,u,v


def yuvFileCut(filePath,width, height,numFrame, startFrame, outPath):
#    """Cut the YUV file at startFrame position for len frames"""
    oneFrameNumBytes = int(width*height*1.5)
    with open(filePath, 'r+b') as file1:

        # header info
        line1 = file1.readline()
        print(line1)

        # string of FRAME 
        line2 = file1.readline()
        print(line2)

        frameByteOffset = len(line1)+(len(line2)+oneFrameNumBytes) * startFrame
        print(frameByteOffset)

        # each frame begins with the 5 bytes 'FRAME' followed by some zero or more characters"
        bytesToRead = (oneFrameNumBytes + len(line2))*numFrame

        file1.seek(frameByteOffset)
        with open(outPath, 'wb') as wfp:
            wfp.write(line1)
            wfp.write(file1.read(bytesToRead))


def yuvFileRead(filePath,width, height,numFrame, startFrame):
#    """Cut the YUV file at startFrame position for len frames"""
    oneFrameNumBytes = int(width*height*1.5)
    with open(filePath, 'r+b') as file1:

        # header info
        line1 = file1.readline()
        print(line1)

        # string of FRAME 
        line2 = file1.readline()
        print(line2)

        frameByteOffset = len(line1)+(len(line2)+oneFrameNumBytes) * startFrame
        print(frameByteOffset)

        # each frame begins with the 5 bytes 'FRAME' followed by some zero or more characters"
        bytesToRead = (oneFrameNumBytes + len(line2))*numFrame

        file1.seek(frameByteOffset)
        y,u,v  = yuv_read(file1,0,height,width) 
        print(y[1:100,:])
        print(np.count_nonzero(y))
        cv2.imwrite('out.png',y)
#yuvFileRead("../all_cut_y4m_vids/EPLDay_AVC_HFR_288p_300K_8.y4m",512,288,0,10)
yuvFileCut(filePath,3840,2160,400,0,'EPLNight_SRC_SRC_SRC_SRC_0.y4m')

