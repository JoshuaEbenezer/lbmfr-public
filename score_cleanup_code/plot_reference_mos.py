import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

scores_df = pd.read_csv('./lbvfr_sepsess_zscore_mos.csv')


def plot_reference(col_vals,col_name):
    scores = []

    for val in col_vals:
        scores.append(scores_df[(scores_df[col_name]==val) & (scores_df['codec']=='SRC')].mos.values)
    scores = np.asarray(scores)
    df2 = pd.DataFrame(scores.T,columns=col_vals)

    meds = df2.median()
    meds.sort_values(ascending=True, inplace=True)
    df2 = df2[meds.index]
    fig = plt.figure(figsize=(32.0, 5.0))
#    fig.set_xticks(arange(1,3,0.5))
    df2.boxplot()
    plt.ylabel('MOS')
    plt.savefig('./plots/reference_mos.png')
content = sorted(scores_df['content'].unique())
plot_reference(content,'content')
