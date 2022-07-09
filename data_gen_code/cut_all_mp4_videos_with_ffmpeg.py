# This code is used to divide videos into 3 groups for the study

import pandas as pd
import sys
import subprocess
import os
import glob




division_csv = pd.read_csv("./shortname_vid_group_divisions.csv")
group1 = division_csv['Group1']
group2 = division_csv['Group2']
group3 = division_csv['Group3']

def cut_video_and_copy(group,index):
    all_commands = []
    old_outfolder = '/data/PV_VQA_Study/all_cut_vids_ss_before_i'
    outfolder = '/data/PV_VQA_Study/all_cut_vids_ss_after_i'
    for vidname in group:
        content_name = vidname.split('_')[0]
        print(content_name)
#        if(content_name!='TNFNFL'):
#            continue
        filenames = glob.glob(os.path.join('../../full_length_distorted_mp4_fullnames',content_name+'*'))
        print(len(filenames))
        for input_vid in filenames:
            print(input_vid)
            if('SRC' in input_vid):
                continue
            begin_time = vidname.split('_')[1]
            extension = os.path.splitext(os.path.basename(input_vid))[1]
            length = 8.00

            old_outname = os.path.join(old_outfolder,os.path.splitext(os.path.basename(input_vid))[0]+'_'+str(begin_time)+extension)
            if(os.path.exists(old_outname)):
                print(old_outname, ' exists')
                continue
            outname = os.path.join(outfolder,os.path.splitext(os.path.basename(input_vid))[0]+'_'+str(begin_time)+extension)
            command = ['./cut_video.sh',input_vid,str(float(begin_time)),str(length),outname]
            print(command)
            all_commands.append(command)
            subprocess.check_call(command)
    print(len(all_commands))

cut_video_and_copy(group1,1)
cut_video_and_copy(group2,2)
cut_video_and_copy(group3,3)




