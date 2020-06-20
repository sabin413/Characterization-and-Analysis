# Author: SA, June 2020
# Checks if the particle-velocity follows MB distribution, needs velocity data from simulation
import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
df = pd.read_pickle('50trajectory_velocity.pkl')#row - atom id, column = time
print(df.shape)
#print(df.head)
print(df.iloc[:,0])
no_of_atoms = df.shape[0]
no_of_snapshots = df.shape[1]

print([no_of_atoms, no_of_snapshots])

def get_list(data, atom_index):#get data of a given atom
	velocity_list = data.iloc[:,atom_index].values #atom index = row, column no is time
	#position_list1 = [[i[-1]] for i in position_list]	#x,y, z co-ords
	return velocity_list

#print (get_list(df, 5000))
vsq_list = []
for i in range(int(1*no_of_snapshots)):
	data_list = get_list(df, i)
	vsq = [np.dot(j,j) for j in data_list]
	vsq_list = vsq_list+vsq
#print(vsq_list)
print(np.mean(vsq_list))
v_list = [np.sqrt(i) for i in vsq_list]
ax = plt.axes()
sns.distplot(v_list, kde = False, norm_hist = True, fit=stats.maxwell)
#plt.hist(wait_time)
ax.set_xlabel('speed', fontsize = 20)
plt.setp(ax.spines.values(), linewidth=1.5)
ax.tick_params(axis='both', which='major', labelsize=18)
plt.tight_layout() 
#plt.savefig('speed_distn_m50.pdf')
plt.show()
