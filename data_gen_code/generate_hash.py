import os
from shutil import copyfile
import glob
import pandas as pd
import random


filenames = glob.glob(os.path.join('../all_cut_y4m_vids','*'))
hash_list = []
for n in filenames:
    extension = os.path.splitext(os.path.basename(n))[1]
    hashname = os.path.join('../hash_vids',str(random.getrandbits(128))+extension)
    print(n,hashname)
    hash_list.append(os.path.basename(hashname))
    copyfile(n,hashname)
file_basenames = [os.path.basename(filenames[i]) for i in range(int(len(filenames)))]
df = pd.DataFrame(list(zip(file_basenames,hash_list)),columns=['original_video_name','hash_video_name'])
outname = 'hash_list.csv'
print(df)
df.to_csv(outname)
