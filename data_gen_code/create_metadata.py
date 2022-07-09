import os
import glob
import pandas as pd

def res_from_content(content):
    if(content=='EPLDay' or content=='EPLNight' ):
        res = '3840x2160'
    elif(content=='TNFF' or content=='TNFNFL' or content=='USOpen'):
        res  = '1280x720'
    elif(content=='Cricket1' or content=='Cricket2'):
        res = '1440x1080'
    return res

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

def expand_res_name(res_shorthand,content):
    print(res_shorthand)
    if(res_shorthand=='720p'):
        resolution='1280x720'
    elif(res_shorthand == '540p'):
        resolution='960x540'
    elif(res_shorthand == '396p'):
        resolution='704x396'
    elif(res_shorthand == '288p'):
        resolution='512x288'
    elif(res_shorthand=='SRC'):
        resolution = res_from_content(content)
    return resolution

hash_df = pd.read_csv('./hash_list.csv')
video_names = hash_df['original_video_name']

content = []
res = []
bitrate = []
fps = []
codec = []
begin_times = []


for vid in video_names:
    split_name = vid.split('_')
    print(split_name)
    content.append(split_name[0])
    codec.append(split_name[1])
    res_shorthand = split_name[3]
    res.append(expand_res_name(res_shorthand,split_name[0]))
    bitrate.append(split_name[4])
    begin_times.append(split_name[5][:-4])
    fr = split_name[2]
    fps.append(fps_from_content(split_name[0],fr))


hash_df['content'] = content
hash_df['fps'] = fps
hash_df['codec']=codec
hash_df['resolution']=res
hash_df['bitrate'] = bitrate
hash_df['begin_time']=begin_times
hash_df.to_csv('./lbvfr_distorted_metadata.csv')
