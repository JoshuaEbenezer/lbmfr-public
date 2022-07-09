import os
import numpy as np
import pandas as pd
import glob

def removeDuplicates(score_df):
    uniqueList = []
    unique_indices = []
    hash_names = score_df['hash_name']
    for index,elem in enumerate(hash_names): 
        if elem not in uniqueList:
            uniqueList.append(elem)
            unique_indices.append(index)
    unique_df = pd.DataFrame([score_df.iloc[i] for i in unique_indices])

    return unique_df

score_csv_list = glob.glob(os.path.join('./scores/','*_1.csv'))

for score_csv in score_csv_list:
    second_score_csv  = score_csv[:-6] +'_2.csv'
    print(second_score_csv)
    subject_id = score_csv.split('_')[-2]
    print(subject_id)
    first_score_df = pd.read_csv(score_csv,header=0,names=['index','hash_name','score'])
    first_score_df['index']=np.arange(len(first_score_df))
    first_score_df['first_session'] = [True]*len(first_score_df)
    first_unique_score_df = removeDuplicates(first_score_df)
    if(os.path.exists(second_score_csv)==False):
        new_score_df = first_score_df
        new_score_df.to_csv(os.path.join('sep_sess_unique_scores/',os.path.basename(score_csv)[:-6]+'.csv'))
        continue
    second_score_df = pd.read_csv(second_score_csv,header=0,names=['index','hash_name','score'])
    second_score_df['index']=np.arange(len(second_score_df))
    second_score_df['first_session'] = [False]*len(second_score_df)
    second_unique_score_df = removeDuplicates(second_score_df)
    new_score_df = pd.concat([first_score_df,second_score_df],ignore_index=True)
    new_score_df.to_csv(os.path.join('sep_sess_unique_scores/',os.path.basename(score_csv)[:-6]+'.csv'))
    print(len(new_score_df))

