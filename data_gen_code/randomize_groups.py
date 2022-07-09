import os
from shutil import copyfile
import glob
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
    print(group_csv_filename)
    group_index = int(os.path.splitext(group_csv_filename)[0][-1])
    print(group_index)
    filenames = list(df['original_video_name'])

    outfolder = '../lists/'
    for index in range(90+(group_index-1)*30+1,90+group_index*30+1):
        temp_list = filenames
        random.seed(index)
        random.shuffle(temp_list)
        print(temp_list)
        flag = 1
        newlist = temp_list
        count = 0
        while(flag):
            newlist,flag = remove_adjacent_content(temp_list)
            print(flag)
            count=count+1
            if(count>20):
                break
        hash_shuffled_list = find_hash(newlist,df)


        list1 = [hash_shuffled_list[i] for i in range(int(len(hash_shuffled_list)//2))]
        list2 = [hash_shuffled_list[i] for i in range(int(len(hash_shuffled_list)//2), len(hash_shuffled_list))]
        newlist1 = [os.path.basename(newlist[i]) for i in range(int(len(newlist)//2))]
        newlist2 = [os.path.basename(newlist[i]) for i in range(int(len(newlist)//2), len(newlist))]

        
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
