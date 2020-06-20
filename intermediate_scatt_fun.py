#Computes intermediate scattering function
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_pickle('50trajectory_data_unit_tau.pkl')#1 column for each snapshot - each element of a column is a list of informations about an atom
#print(df.head())
print(df.shape)#no of atoms by no of snapshots
no_of_atoms = df.shape[0]
no_of_snapshots = df.shape[1]
#print(df.iloc[:,0])
time_step = 0.001*200
def get_list(data, atom_index):#obtains a row from a dataframe named data
	position_list = data.iloc[atom_index].values
	position_list1 = [i[2:] for i in position_list]	
	return position_list1

#print(get_list(df, 0))	


def int_corr(q,t):
	ans_list = []
	for atom_index in range(no_of_atoms):
		pos_list = get_list(df, atom_index)
		if t == 0:
			r0_list = pos_list
			rt_list = pos_list
		else:
			r0_list = pos_list[:-t]
			rt_list = pos_list[t:]
		#r0_list = pos_list[:-t]
		#rt_list = pos_list[t:]
 		rt_minus_ro= [np.subtract(np.array(a[1]), np.array(a[0])) for a in zip(r0_list,rt_list)]
		q = np.array(q)
		cosq_dot_r_list = ([np.cos(np.dot(q,r)) for r in rt_minus_ro])
 		ans = np.mean(cosq_dot_r_list)
		ans_list.append(ans)
		#print(ans)
	return np.mean(ans_list)

#print(int_corr([1,2,3], 2))
t_list = np.arange(0, int(no_of_snapshots), 1)#range(0,int(0.4*no_of_snapshots))
#t_list
pi = np.pi
fqt_list = []

#for t in t_list:
#	cor = int_corr([0.5,0.0,0.0], t)
#	fqt_list.append(cor)
#	print(t, cor)
#t_list_plot = [i*time_step for i in t_list]#range(0,int(0.4*no_of_snapshots))
ax = plt.axes()
#ax.scatter(t_list, [i[-1] for i in get_list(df, 0)])
ax.plot(t_list[:5000], [i[-1] for i in get_list(df, 3)][:5000])

#ax.set_xscale('symlog')
plt.show()
