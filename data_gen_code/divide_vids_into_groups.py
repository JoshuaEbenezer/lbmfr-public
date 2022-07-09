# This code is used to divide videos into 3 groups for the study

import pandas as pd
import sys
import subprocess
import os
import glob




division_csv = pd.read_csv("../shortname_vid_group_divisions.csv")
hash_csv = pd.read_csv('./hash_list.csv')
original_video_names = hash_csv['original_video_name']
hash_names = hash_csv['hash_video_name']

group1 = division_csv['Group1']
group2 = division_csv['Group2']
group3 = division_csv['Group3']

def divide(group,index):
    all_commands = []
    outname_list = []
    hash_name_list = []
    for vidname in group:
        content_name = vidname.split('_')[0]
        begin_time = vidname.split('_')[1]
        print(len(group),content_name,begin_time)
        filenames = glob.glob(os.path.join('../all_cut_y4m_vids',content_name+'*_'+begin_time+'.y4m'))
        print(len(filenames))
        for input_vid in filenames:
            hash_name = hash_csv[hash_csv["original_video_name"]==os.path.basename(input_vid)].hash_video_name.iloc[0]
            print(input_vid,hash_name)
            hash_name_list.append(hash_name)
            outname_list.append(os.path.basename(input_vid))
    return list(zip(outname_list,hash_name_list))

d1 = divide(group1,1)
d2 = divide(group2,2)
d3 = divide(group3,3)

df1 = pd.DataFrame(d1,columns=['original_video_name','hash_video_name'])
df1.to_csv('group1.csv')
df2 = pd.DataFrame(d2,columns=['original_video_name','hash_video_name'])
df2.to_csv('group2.csv')
df3 = pd.DataFrame(d3,columns=['original_video_name','hash_video_name'])
df3.to_csv('group3.csv')


