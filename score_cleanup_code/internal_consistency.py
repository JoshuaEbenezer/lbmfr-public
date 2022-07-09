import os
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
import numpy as np
from collections import defaultdict
import glob
import pandas as pd

filenames = glob.glob(os.path.join('./mos_sepsess_zscores','*.csv'))

video_dict = defaultdict(list)

for subject_csv in filenames:
    subject_df = pd.read_csv(subject_csv)
    video_names = subject_df['video']
    for index,v in enumerate(video_names):
        score = subject_df['raw_mos_zscore'].iloc[index]
        vkey = os.path.splitext(v)[0]
        print(vkey,subject_csv)
        video_dict[vkey].append(score)



print(video_dict)
print(len(video_dict))
scores = []
names = []
content = []
codec = []
fr = []
res = []
bitrate = [] 
srocc =[]


for rand_seed in range(100):
    np.random.seed(rand_seed)
    group1 = []
    group2 = []
    for key,val in video_dict.items():
        print(key)
        print(len(val))
        #if(len(val)<20):
        #    continue
        split_name = key.split('_')
        group1_indices = np.random.randint(low=0,high=len(val),size=len(val)//2)
        group2_indices = np.asarray(np.delete(np.arange(len(val)),group1_indices),dtype=int)
        print(group1_indices)
        print(group2_indices)
        print(np.arange(len(val)))
        group1_scores = np.asarray(val)[group1_indices]
        group2_scores = np.asarray(val)[group2_indices]
        group1.append(np.mean(group1_scores))
        group2.append(np.mean(group2_scores))
    group_srocc = spearmanr(group1,group2)
    srocc.append(group_srocc[0])
    plt.figure()
    plt.scatter(group1,group2)
    plt.title('Split '+str(rand_seed))
    plt.savefig('./plots/internal_consistency/'+str(rand_seed)+'.png')
    plt.close()

#    names.append(key)
#    content.append(split_name[0]+'_'+split_name[-1])
#    codec.append(split_name[1])
#    fr.append(split_name[2])
#    res.append(split_name[3])
#    if(split_name[4]=='SRC'):
#        bitrate.append(100000)
#    else:
#        bitrate.append(split_name[4][:-1])
print(srocc)
print(np.median(srocc))
print(np.std(srocc))
