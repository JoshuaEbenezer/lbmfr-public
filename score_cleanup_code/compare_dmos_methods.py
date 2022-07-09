import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import spearmanr

dmos1_df = pd.read_csv('./lbvfr_dmos.csv')
dmos2_df = pd.read_csv('./lbvfr_dmos_from_mos.csv')

sorted_dmos1_df = dmos1_df.sort_values('video')
print(sorted_dmos1_df)
sorted_dmos2_df = dmos2_df.sort_values('video')
print(sorted_dmos2_df)

dmos1 = sorted_dmos1_df['dmos']
dmos2 = sorted_dmos2_df['dmos']
srocc = spearmanr(dmos1,dmos2)
rmse = np.sqrt(np.mean((dmos1-dmos2)**2))
print(np.mean(dmos1),np.mean(dmos2))
print(srocc)
print(rmse)
plt.figure()
plt.hist(dmos1,bins='auto')
plt.savefig('./plots/dmos_mdos_hist.png')
plt.close()
plt.figure()
plt.hist(dmos2,bins='auto')
plt.savefig('./plots/dmos_from_mos_hist.png')
plt.close()
