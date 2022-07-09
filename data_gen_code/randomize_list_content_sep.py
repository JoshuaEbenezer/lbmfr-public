import os
from shutil import copyfile
import glob
import numpy as np
import pandas as pd
import random

def swapPositions(vidlist, pos1, pos2):
     
    vidlist[pos1], vidlist[pos2] = vidlist[pos2], vidlist[pos1]
    return vidlist

def remove_adjacent_content(vidlist):
    flag = 0
    newlist = vidlist
    for i in range(len(vidlist)-2):
        if(vidlist[i].split('_')[0]==vidlist[i+1].split('_')[0] and vidlist[i].split('_')[-1]==vidlist[i+1].split('_')[-1]):
            print(vidlist[i],vidlist[i+1])
            print('adjacent content, moving')
            swapPositions(newlist,i+1,i+2) 
            flag = 1
    return newlist,flag
def shuffle_list(filenames,index):
    temp_list = filenames 
    random.seed(index)
    random.shuffle(temp_list)
    flag = 1
    newlist = temp_list
    count = 0


    while(flag):
        newlist,flag = remove_adjacent_content(temp_list)
        print(flag)
        count=count+1
        if(count>20):
            break
    return newlist
def find_hash(newlist,df):
    hash_list = list(df['hash_video_name'])
    filenames = list(df['original_video_name'])
    hash_shuffled_list = []
    for n in newlist:
        print(n)
        hash_val = hash_list[filenames.index(n)]
        print(hash_val)
        hash_shuffled_list.append(hash_val)
    return hash_shuffled_list


def randomize_group(group_csv_filename):
    df = pd.read_csv(group_csv_filename)
    group_index = int(os.path.splitext(group_csv_filename)[0][-1])
    filenames = list(df['original_video_name'])
    randnums  =random.sample(range(10), 10)
    first_half = randnums[:5]
    second_half = randnums[5:]
    first_half_vids  = []
    second_half_vids = []
    for content_id in first_half:
        vids = filenames[content_id*25:(content_id+1)*25]
        first_half_vids.extend(vids) 
    for content_id in second_half:
        vids = filenames[content_id*25:(content_id+1)*25]
        second_half_vids.extend(vids) 

    outfolder = '../content_sep_list_subjects_after_90/'
    for index in range(90+(group_index-1)*30+1,90+group_index*30+1):
        newlist1 = shuffle_list(first_half_vids,index)
        newlist2 = shuffle_list(second_half_vids,index)
        print(newlist1)
        print('above is first half')
        print(newlist2)
        print('above is second half')
        list1 = find_hash(newlist1,df)
        list2 = find_hash(newlist2,df)

#        newlist1 = [os.path.basename(newlist[i]) for i in range(int(len(newlist)//2))]
#        newlist2 = [os.path.basename(newlist[i]) for i in range(int(len(newlist)//2), len(newlist))]



        
        df1 = pd.DataFrame(list(zip(newlist1,list1)),columns=['original_video_name','hash_video_name'])
        df2 = pd.DataFrame(list(zip(newlist2,list2)),columns=['original_video_name','hash_video_name'])
        outname1 = os.path.join(outfolder,'list_{}_{}.csv'.format(index,1))
        outname2 = os.path.join(outfolder,'list_{}_{}.csv'.format(index,2))
        print(outname1,outname2)
        print(df1,df2)
        df1.to_csv(outname1)
        df2.to_csv(outname2)
randomize_group('group1.csv')
randomize_group('group2.csv')
randomize_group('group3.csv')
