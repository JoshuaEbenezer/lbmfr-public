import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
import glob

scores_df = pd.read_csv('./sureal/lbmfr_sureal_scores.csv')
scores_df = scores_df[~scores_df.video.str.contains('SRC')]
scores_df['content'] = [v.split('_')[0]+'_'+v.split('_')[-1] for v in scores_df['video']]
scores_df['codec'] = [v.split('_')[1] for v in scores_df['video']]
scores_df['fr'] = [v.split('_')[2] for v in scores_df['video']]
scores_df['res'] = [v.split('_')[3] for v in scores_df['video']]
scores_df['bitrate'] = [int(v.split('_')[4][:-1]) for v in scores_df['video']]

bitrates = [b for b in scores_df['bitrate'] if (b!='SRC')]
unique_bitrates = list(set(bitrates))

codec = sorted(scores_df['codec'].unique())
content = sorted(scores_df['content'].unique())
fr = scores_df['fr'].unique()
res = sorted(scores_df['res'].unique())
bitrate = sorted(unique_bitrates,key=int)


def plot_by_col(col_vals,col_name,xlabel):
    scores = []
    for val in col_vals:
        scores.append(scores_df[scores_df[col_name]==val].dmos.values)
    plt.figure()
    plt.clf()
    plt.boxplot(scores,labels=col_vals)
    plt.xlabel(xlabel)
    plt.ylabel('DMOS')
    #plt.show()
    plt.savefig('./plots/sureal/plotbycol/'+col_name+'.png')
    #plt.close()
    return
def plot_by_twocol(col_vals,col_name,col_vals2,col_name2):
    scores = []
    col_val_list = []
    for val in col_vals:
        for val2 in col_vals2:
            scores.append(scores_df[(scores_df[col_name]==val) & (scores_df[col_name2]==val2) ].dmos.values)
            col_val_list.append(val+' '+val2)
    plt.figure()
    plt.clf()
    plt.boxplot(scores,labels=col_val_list)
    plt.xlabel('Codec and Frame Rate')
    plt.ylabel('DMOS')
    #plt.show()
    plt.savefig('./plots/sureal/plotbycol/'+col_name+'_'+col_name2+'.png')
    #plt.close()
    return

plot_by_twocol(codec,'codec',fr,'fr')
plot_by_col(content,'content','Content')
plot_by_col(res,'res','Resolution')
plot_by_col(codec,'codec','Codec')
plot_by_col(bitrate,'bitrate','Bitrate')
plot_by_col(fr,'fr','Frame Rate')
#

def sort_by_x(x,y):
    new_x, new_y = zip(*sorted(zip(x, y)))
    return new_x,new_y
def plot_by_fr(col_vals,col_name,codec):
    for val in col_vals:
        hfr_bitrates = scores_df[(scores_df[col_name]==val) & (scores_df['fr']=='HFR')& (scores_df['codec']==codec)].bitrate.values
        sfr_bitrates = scores_df[(scores_df[col_name]==val) & (scores_df['fr']=='SFR')& (scores_df['codec']==codec)].bitrate.values
        if(len(sfr_bitrates)<6 or len(hfr_bitrates)<6):
            continue
        hfr_scores = -scores_df[(scores_df[col_name]==val) & (scores_df['fr']=='HFR')& (scores_df['codec']==codec)].dmos.values
        sfr_scores = -scores_df[(scores_df[col_name]==val) & (scores_df['fr']=='SFR')& (scores_df['codec']==codec)].dmos.values
        sfr_bitrates,sfr_scores = sort_by_x(sfr_bitrates,sfr_scores)
        hfr_bitrates,hfr_scores = sort_by_x(hfr_bitrates,hfr_scores)
        res_vals = ['288p','396p','396p','540p','540p','720p']
        plt.figure()
        plt.plot(hfr_bitrates,hfr_scores,'g+',color='green',linestyle='dashed')
        #for i,txt in enumerate(res_vals):
        #    plt.annotate(txt, (hfr_bitrates[i], hfr_scores[i]))
        plt.plot(sfr_bitrates,sfr_scores,'r+',color='red',linestyle='dashed')
        #for i,txt in enumerate(res_vals):
        #    plt.annotate(txt, (sfr_bitrates[i], sfr_scores[i]))
        plt.legend(["HFR","SFR"])
        plt.xlabel('Bitrate (kbps)')
        plt.ylabel('DMOS')
#        plt.title(val)
        plt.savefig('./plots/sureal/plotbycol/dmos_HFR_v_SFR_'+codec+'_'+val+'.png')
        plt.close()
#        plt.show()
def plot_by_fr_bothcodec(col_vals,col_name):
    for val in col_vals:
        codec = 'HEVC'
        hfr_bitrates = scores_df[(scores_df[col_name]==val) & (scores_df['fr']=='HFR')& (scores_df['codec']==codec)].bitrate.values
        sfr_bitrates = scores_df[(scores_df[col_name]==val) & (scores_df['fr']=='SFR')& (scores_df['codec']==codec)].bitrate.values
        if(len(sfr_bitrates)<6 or len(hfr_bitrates)<6):
            continue
        hfr_scores = -scores_df[(scores_df[col_name]==val) & (scores_df['fr']=='HFR')& (scores_df['codec']==codec)].dmos.values
        sfr_scores = -scores_df[(scores_df[col_name]==val) & (scores_df['fr']=='SFR')& (scores_df['codec']==codec)].dmos.values
        sfr_bitrates,sfr_scores = sort_by_x(sfr_bitrates,sfr_scores)
        hfr_bitrates,hfr_scores = sort_by_x(hfr_bitrates,hfr_scores)
        res_vals = ['288p','396p','396p','540p','540p','720p']
        plt.figure()
        plt.plot(hfr_bitrates,hfr_scores,'g+',color='green',linestyle='dashed')
        #for i,txt in enumerate(res_vals):
        #    plt.annotate(txt, (hfr_bitrates[i], hfr_scores[i]))
        plt.plot(sfr_bitrates,sfr_scores,'r+',color='red',linestyle='dashed')
        #for i,txt in enumerate(res_vals):
        #    plt.annotate(txt, (sfr_bitrates[i], sfr_scores[i]))
        codec = 'AVC'
        hfr_bitrates = scores_df[(scores_df[col_name]==val) & (scores_df['fr']=='HFR')& (scores_df['codec']==codec)].bitrate.values
        sfr_bitrates = scores_df[(scores_df[col_name]==val) & (scores_df['fr']=='SFR')& (scores_df['codec']==codec)].bitrate.values
        if(len(sfr_bitrates)<6 or len(hfr_bitrates)<6):
            continue
        hfr_scores = -scores_df[(scores_df[col_name]==val) & (scores_df['fr']=='HFR')& (scores_df['codec']==codec)].dmos.values
        sfr_scores = -scores_df[(scores_df[col_name]==val) & (scores_df['fr']=='SFR')& (scores_df['codec']==codec)].dmos.values
        sfr_bitrates,sfr_scores = sort_by_x(sfr_bitrates,sfr_scores)
        hfr_bitrates,hfr_scores = sort_by_x(hfr_bitrates,hfr_scores)
        plt.plot(hfr_bitrates,hfr_scores,'b+',color='blue',linestyle='dashed')
        #for i,txt in enumerate(res_vals):
        #    plt.annotate(txt, (hfr_bitrates[i], hfr_scores[i]))
        plt.plot(sfr_bitrates,sfr_scores,'m+',color='magenta',linestyle='dashed')
        #for i,txt in enumerate(res_vals):
        #    plt.annotate(txt, (sfr_bitrates[i], sfr_scores[i]))
        plt.legend(["HEVC HFR","HEVC SFR","AVC HFR", "AVC SFR"])
        plt.xlabel('Bitrate (kbps)')
        plt.ylabel('-DMOS')
        plt.title(val)
        plt.savefig('./plots/sureal/'+val+'.png')
        plt.close()
    return
#plot_by_fr_bothcodec(content,'content')
#
#plot_by_fr(fr,'fr','HEVC')
#plot_by_fr(content,'content','AVC')
#res_fr_scores = []
#res_fr_bitrates = []
#names = []
#for res_val in res:
#    for frame_rate in fr:
#        res_fr_scores.append(np.mean(scores_df[(scores_df['res']==res_val) & (scores_df['fr']==frame_rate)].dmos.values))
#        res_fr_bitrates.append(np.mean(scores_df[(scores_df['res']==res_val) & (scores_df['fr']==frame_rate)].bitrate.values))
#        names.append(res_val+frame_rate)
#res_fr_bitrates,res_fr_scores = sort_by_x(res_fr_bitrates,res_fr_scores)
#fig = plt.figure(figsize=(32.0, 5.0))
#plt.plot(res_fr_bitrates,res_fr_scores,'b+',color='blue',linestyle='dashed')
#
#plt.xticks(res_fr_bitrates,labels=names)
#plt.savefig('./plots/res_fr_dmos.png')
#plt.close()
