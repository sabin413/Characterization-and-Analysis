import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
#df = pd.read_csv('df_autocorr.csv', index_col = None)
df = pd.read_csv('df_autocorr25.csv', index_col = None)
print (df.head)

#density = df.iloc[50].values[2:]
time = range(0, 1000)#len(density)-950)

#mean = np.mean(density)
#sq_mean = np.mean([(i-mean)**2 for i in density])

def self_corr(lis,t):
	#n = len(lis)
	mean_value = np.mean(lis)
	lis1 = [(i-mean_value) for i in lis]
	normalize = np.mean([e**2 for e in lis1])
	if t == 0:
		new_list1 = lis1
		new_list2 = lis1
	else:
		new_list1 = lis1[:-t]
		new_list2 = lis1[t:]
	ans =[a[0]*a[1] for a in zip(new_list1,new_list2)]
	ans_norm = (1/normalize)*np.mean(ans)
	return ans_norm

##correlated data
#density_list = [[random.uniform(0,1) for i in range(10000)]]



## plot
density_list = [df.iloc[i].values[2:] for i in [7,  50]]
time_step = 0.005*2
#time = [i*time_step for i in time]

for density in density_list:
	time = range(0, 2000)
	corr_list = [self_corr(density, i) for i in time]
	#print(time[:3],corr_list[:3])
	ax = plt.axes()
	time = [i*time_step for i in time]
	#ax.plot(time, corr_list)
	ax.set_xscale('symlog')
	ax.scatter(time, corr_list)
ax.set_xlabel(r'$t$', {'fontsize': 22})
ax.set_ylabel(r'$<c(0).c(t)>$', { 'fontsize': 22})
plt.tight_layout()

plt.legend((r'$near-the -wall$',r'$far$', r'$z50$', r'$z25$',r'$z35$', r'$z50$'),
          shadow=False, loc=(0.38, 0.48), handlelength=1.5, fontsize=13)
plt.savefig('dynamic_corr.pdf')
plt.show()
