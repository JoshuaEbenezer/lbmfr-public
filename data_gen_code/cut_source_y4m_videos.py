
import pandas as pd
import sys
import subprocess
import os
import glob




division_csv = pd.read_csv("../shortname_vid_group_divisions.csv")
group1 = division_csv['Group1']
group2 = division_csv['Group2']
group3 = division_csv['Group3']

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
    return fps

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

def y4mFileCut(filePath,width, height,startFrame,numFrame, outPath):
#    """Cut the YUV file at startFrame position for numFrame frames"""
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
    return


    

def cut_video_and_copy(group,index):
    all_commands = []
    outfolder = '../cut_source_vids' 
    for vidname in group:
        content_name = vidname.split('_')[0]
        filenames = glob.glob(os.path.join('../source_y4m',content_name+'*'))
        for input_vid in filenames:
            begin_time = int(vidname.split('_')[1])
            base = os.path.basename(input_vid)
            print(content_name,begin_time)
            if(content_name=='TNFNFL'):
                continue
            elif(content_name=='Cricket1' or content_name=='Cricket2'):
                resolution='1440x1080'
                fps = 50
            elif(content_name=='EPLDay' or content_name=='EPLNight'):
                resolution='3840x2160'
                fps = 50
            elif(content_name=='USOpen'):
                resolution='1920x1080'
                fps = 50
            elif(content_name=='TNFF'):
                resolution='1280x720'
                fps = 59.94

            extension = os.path.splitext(os.path.basename(input_vid))[1]

            width = int(resolution.split('x')[0])
            height = int(resolution.split('x')[1])
            startFrame = int(begin_time*fps)
            length = int(8*fps) 
            outname = os.path.join(outfolder,content_name+'_SRC_SRC_SRC_SRC_'+str(begin_time)+extension)
            print(input_vid,width,height,length,startFrame,begin_time,fps,outname)
#            if(os.path.exists(outname)):
#                continue
            y4mFileCut(input_vid,width,height,startFrame,length,outname)

cut_video_and_copy(group1,1)
cut_video_and_copy(group2,2)
cut_video_and_copy(group3,3)




