# Author: SA, October 2019
# reads lammps data, multiple snapshots are stored as values of a dictionary - keys: time, values: data -
# stored as a pandas dataframe
# this is useful when we want to compute dynamic quantities

import numpy as np
import pandas as pd

#get atom_no and starting time-step
f = open('40sbrush.lammpstrj','r')
big_string = f.read()
big_list0 = big_string.split("ITEM: TIMESTEP")
#print(big_list0[0])
big_list = big_list0[1:] #to remove the first empty space - big_list is a list of strings, each string 
#is one snap-shot
print(len(big_list))
f.close()

#print(big_list[0].splitlines()[9])
#ignore first 9 lines
dict_df = {}
ind = 1
for big_string in big_list:
	#print(ind)
	position_list = []
	big_string1 = big_string.rstrip()
	#print(big_string1)
	line_list = big_string1.split('\n')
	#print(line_list)
	for i in line_list[9:]:
		lst0 = i.split()
		#print(lst0)
		lst1 = [float(i) for i in lst0]
		position_list.append(lst1)
	solvent_position_list = [i for i in position_list if i[1]==7]#keep only what I need
	solvent_position_list.sort(key=lambda x: x[0])
	dict_df['col{}'.format(ind)] = solvent_position_list
	ind= ind+1
	print(len(solvent_position_list))

#print(dict_df[1])
df = pd.DataFrame.from_dict(dict_df)
print(df.columns)
#print(df[1])
df.to_csv('position_data.csv')	
