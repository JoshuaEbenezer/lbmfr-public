from scipy.ndimage import sobel
from joblib import dump,load
import matplotlib.pyplot as plt
import numpy as np
import os
import glob

def res_from_content(content):
    if(content=='EPLDay' or content=='EPLNight' ):
        res = '3840x2160'
    elif(content=='TNFF' or content=='TNFNFL' or content=='USOpen'):
        res  = '1280x720'
    elif(content=='Cricket1' or content=='Cricket2'):
        res = '1440x1080'

    return res 

def expand_res_name(res_shorthand):
    print(res_shorthand)
    if(res_shorthand=='720p'):
        resolution='1280x720'
    elif(res_shorthand == '540p'):
        resolution='960x540'
    elif(res_shorthand == '396p'):
        resolution='704x396'
    elif(res_shorthand == '288p'):
        resolution='512x288'
    return resolution
def length_from_content(content):

    if(content=='EPLDay' or content=='EPLNight' or content=='Cricket1' or content=='Cricket2' or content=='USOpen'):
        length = 400
    elif(content=='TNFF' or content=='TNFNFL'):
        length  = 479
    return length
def fread(fid, nelements, dtype):
     if dtype is str:
         dt = np.uint8  # WARNING: assuming 8-bit ASCII for np.str!
     else:
         dt = dtype

     data_array = np.fromfile(fid, dt, nelements)
     data_array.shape = (nelements, 1)

     return data_array


def sobel_mag(frame):
    x= sobel(frame,0)
    y = sobel(frame,1)
    mag = np.hypot(x,y)
    return mag



def si_and_ti(filePath,width, height,numFrame):
#    """Cut the YUV file at startFrame position for len frames"""
    oneFrameNumBytes = int(width*height*1.5)
    with open(filePath, 'r+b') as file1:

        # header info
        line1 = file1.readline()
        print(line1)

        # string of FRAME 
        line2 = file1.readline()

        startFrame = 0
        frameByteOffset = len(line1)+(len(line2)+oneFrameNumBytes) * startFrame + len(line2)
        print(frameByteOffset)

        # each frame begins with the 5 bytes 'FRAME' followed by some zero or more characters"
        bytesToRead = int(oneFrameNumBytes/1.5)

        file1.seek(frameByteOffset)
        prev_y  = fread(file1,height*width,np.uint8)

        space_std_sobel = []
        time_std_sobel = []

        for startFrame in range(1,length):
            frameByteOffset = len(line1)+(len(line2)+oneFrameNumBytes) * startFrame + len(line2)

            # each frame begins with the 5 bytes 'FRAME' followed by some zero or more characters"
            bytesToRead = int(oneFrameNumBytes/1.5)

            file1.seek(frameByteOffset)
            curr_y  = fread(file1,height*width,np.uint8)
            frame_diff = curr_y-prev_y
            space_sobel_out = sobel_mag(curr_y.astype(np.float32))
            time_sobel_out = sobel_mag(frame_diff.astype(np.float32))

            si = np.std(space_sobel_out)
            ti = np.std(time_sobel_out)
            print(si,ti)
            space_std_sobel.append(si)
            time_std_sobel.append(ti)

            prev_y = curr_y
        
        return np.max(space_std_sobel),np.max(time_std_sobel)


filenames = glob.glob(os.path.join('../cut_source_vids','*'))
all_si = []
all_ti = []
#for input_vid in filenames:
#    vidname = os.path.basename(input_vid)
#    content_name = vidname.split('_')[0]
#    
#    base = os.path.basename(input_vid)
#    print(content_name)
#    extension = os.path.splitext(os.path.basename(input_vid))[1]
#    fr = base.split('_')[-3]
#    resolution = res_from_content(content_name) 
#    print(resolution)
#
#    width = int(resolution.split('x')[0])
#    height = int(resolution.split('x')[1])
#
#    length = length_from_content(content_name)
#    print(input_vid,width,height,length)
##            if(os.path.exists(outname)):
##                continue
#    si,ti = si_and_ti(input_vid,width,height,length)
#    print(si,ti)
#    all_si.append(si)
#    all_ti.append(ti)

#X = {'SI':all_si,'TI':all_ti,'filenames':filenames}
#dump(X,'si_and_ti.z')
X = load('si_and_ti.z')
si = X['SI']
ti = X['TI']

plt.scatter(ti,si)
plt.savefig('SI_vs_TI.png')

