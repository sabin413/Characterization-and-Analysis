import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_pickle('50trajectory_data_unit_tau.pkl')
#df = pd.read_pickle('50trajectory_data_02tau.pkl')
#1 column for each snapshot - each element of a column is a list of informations about an atom
#print(df.head())
print(df.shape)#no of atoms by no of snapshots
no_of_atoms = df.shape[0]
no_of_snapshots = df.shape[1]
#print(df.iloc[:,0])
time_step = 0.001*1000
brush_width = 10.64
##
def get_zlist(data, atom_index):#obtains z positions from a dataframe named data
	position_list = data.iloc[atom_index].values
	position_list1 = [i[-1] for i in position_list]	
	return position_list1
#print(get_zlist(df,0))
##symbolize the z data by 1,2,3
def sym(x):
	lo = 0
	up = brush_width
	threshold = 2
	if x<threshold:
		symb = 1
	elif x>(up-threshold):
		symb = 3
	else:
		symb = 2
	return symb
#symb_list = [sym(i) for i in get_zlist(df,4)]
#print(symb_list)
## get the first pair of points - wait time and flight time
def get_locations(lis):
	lis1 = []
	#sub_lis = [1,3]# assumes that the atom is initially close to a wall
	s1 = lis[0]
	#print(s1)
	s2 = 3
	if s1==3:
		s2 = 1
	#print(s2)

	for i in lis:
		if i == s2:
			l1 = lis.index(i)
			break
	lis2 = lis[:l1][::-1]
	for j in lis2:
		if j == s1:
			l2 = lis2.index(j)
			break
	return ([l1-l2,l2]) #(wait_time, flight_time)

#print(get_locations(symb_list))

##
def get_answer_given_atom(data,atom_index):
	ans_list = []
	z_list = get_zlist(data, atom_index)
	symb_list = [sym(i) for i in z_list]
	for elem in symb_list:
		if elem==1 or elem==3:
			new_start = symb_list.index(elem)
			symb_list = symb_list[new_start:]
			break
	while len(symb_list)>7000:
		locations = get_locations(symb_list)
		ans_list.append(locations)
		numb = locations[0]+locations[1]
		symb_list = symb_list[numb:]
	return(ans_list)
#for i in range(3,4):
#	print(i, get_answer_given_atom(df,i))
#print(sum([a[1] for a in ans_list]))

wait_time = []
flight_time = []
for atoms in range(0,20):
	ans_i = get_answer_given_atom(df, atoms)
	w_list = [ans[0] for ans in ans_i]
	f_list = [ans[1] for ans in ans_i]
	wait_time = wait_time+w_list
	flight_time = flight_time+f_list
print(np.min(wait_time), np.min(flight_time))
#print(sorted(flight_time))
ax = plt.axes()
sns.distplot(flight_time, kde = False)
#plt.hist(wait_time)
ax.set_xlabel('hopping time', fontsize = 20)
plt.setp(ax.spines.values(), linewidth=1.5)
ax.tick_params(axis='both', which='major', labelsize=18)
plt.tight_layout() 
plt.savefig('hopping_time_sigma50_m50.pdf')
plt.show()
	
		

	

