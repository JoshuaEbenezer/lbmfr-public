import pandas as pd
from ast import literal_eval
import json

db_df = pd.read_csv('./lbvfr_for_sureal_group3.csv')

json_db = {}
json_db['ref_videos']=[]
json_db['dis_videos']=[]

ref_count = 0
dis_count = 0

unique_contents = list(db_df['content'].unique())


include_ref = True
for index, row in db_df.iterrows():
    
    scores = literal_eval(row['mos_list'])
    subject_ids = literal_eval(row['subject_ids'])
    zipbObj = zip(subject_ids, scores)
    dict_scores= dict(zipbObj)

    if(row['fr']=='SRC'):
        json_db['ref_videos'].append({'content_id': unique_contents.index(row['content']), 'content_name': row['content'],\
                'path': row['video']})
        ref_count+=1
        if(include_ref):
            json_db['dis_videos'].append({'content_id': unique_contents.index(row['content']), 'asset_id': dis_count,\
                    'os':dict_scores,'path': row['video']})
            dis_count+=1
    else:
        json_db['dis_videos'].append({'content_id': unique_contents.index(row['content']), 'asset_id': dis_count,\
                'os':dict_scores,'path': row['video']})
        dis_count+=1

print(len(json_db['dis_videos']))
with open('lbmfr_group3_withref.json', 'w') as outfile:
    json.dump(json_db, outfile)
