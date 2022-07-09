import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import glob

scores_df = pd.read_csv('./lbvfr_mos.csv')

codec = sorted(scores_df['codec'].unique())
content = sorted(scores_df['content'].unique())
fr = scores_df['fr'].unique()
res = sorted(scores_df['res'].unique())
bitrate = sorted(scores_df['bitrate'].unique(),key=int)


def plot_by_col(col_vals,col_name):
    scores = []
    for val in col_vals:
        scores.append(scores_df[scores_df[col_name]==val].mos.values)
    plt.boxplot(scores,labels=col_vals)
    plt.xlabel(col_name)
    plt.ylabel('MOS')
    plt.show()

#plot_by_col(content,'content')
#plot_by_col(res,'res')
#plot_by_col(codec,'codec')
#plot_by_col(bitrate,'bitrate')
#plot_by_col(fr,'fr')
#

def sort_by_x(x,y):
    new_x, new_y = zip(*sorted(zip(x, y)))
    return new_x,new_y
def plot_by_fr(col_vals,col_name):
    for val in col_vals:
        hfr_bitrates = scores_df[(scores_df[col_name]==val) & (scores_df['fr']=='HFR')& (scores_df['codec']=='AVC')].bitrate.values
        sfr_bitrates = scores_df[(scores_df[col_name]==val) & (scores_df['fr']=='SFR')& (scores_df['codec']=='AVC')].bitrate.values
        hfr_scores = scores_df[(scores_df[col_name]==val) & (scores_df['fr']=='HFR')& (scores_df['codec']=='AVC')].mos.values
        sfr_scores = scores_df[(scores_df[col_name]==val) & (scores_df['fr']=='SFR')& (scores_df['codec']=='AVC')].mos.values
        sfr_bitrates,sfr_scores = sort_by_x(sfr_bitrates,sfr_scores)
        hfr_bitrates,hfr_scores = sort_by_x(hfr_bitrates,hfr_scores)
        plt.figure()
        plt.plot(hfr_bitrates,hfr_scores,'g+',color='green',linestyle='dashed')
        plt.plot(sfr_bitrates,sfr_scores,'r+',color='red',linestyle='dashed')
        plt.legend(["HFR","SFR"])
        plt.xlabel('Bitrate (kbps)')
        plt.ylabel('MOS')
        plt.title(val)
        plt.savefig('./plots/HFR_v_SFR/'+val+'.png')
        plt.close()
#        plt.show()

plot_by_fr(content,'content')
