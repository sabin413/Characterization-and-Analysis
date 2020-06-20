# Author: SA, November 2019
# finds the density profile of chain-ends by using several time-steps (after equilibration) of a single trajectory 
# saves the density profile for each time step as a column of a DataFrame, one of the columns is z-coordinate
# the most interesting thing about this code is *the way it does binning*

import numpy as np
import pandas as pd

#get atom_no and starting tim-step
sigma_lis = [25, 333, 50, 66]
df = pd.DataFrame()
for sigma in sigma_lis
	f = open('{}srun/brush.lammpstrj'.format(sigma),'r')
	for i in range(20):
		line = f.readline()
		field = line.strip()#removes characters from both left and right ends
		#print(field)
		if field =="ITEM: TIMESTEP":
			time_step = int(f.readline())
		if field =="ITEM: NUMBER OF ATOMS":
			atom_no = int(f.readline())
	f.close()

	start = 9 # to ignore first 9 lines 
	traj_no = 1000
	print(time_step, atom_no)
	binsize = 10.64/52

	f = open('40sbrush.lammpstrj','r')	
	df1 = pd.DataFrame()
	for t in range(1,traj_no+1):
		flag = 'off'
		lst = []
		for i in range(atom_no+start-1):
			line = f.readline()
			field = line.strip()#removes characters from both left and right ends
			#print(field)
			if field =="ITEM: TIMESTEP":
				time_step = int(f.readline()) #note that this makes the total no of elements in the list n-1	
				#print(time_step)
			if field =="ITEM: ATOMS id type x y z":
				flag = 'on'
				continue	
			if flag == 'on':
				clearField = field.split(" ") # splits strings separated by whitespaces
				values = [float(i) for i in clearField]
				lst.append(values)
		print(t,len(lst))
		
		lstZ_e = [i[-1] for i in lst if i[1]==7] # ends monomers
		lstSorted1 = sorted(lstZ_e)
		#print(lstSorted[-1])
		binsize = 10.64/52
		area = 1000
		lst1 = np.arange(0, 10.64, binsize)
		freqList1 = []
		for i in lst1:
			count = 0
			for j in lstSorted1[sum(freqList1):]:
				if j>=i+binsize:
					break
				count = count+1
			freqList1.append(count)
		#print(freqList1)
		freqList1_n = np.array(freqList1)#1.0/binsize*1.0/(area)*(np.array(freqList1))
		
		
		df1['zPosition'] = lst1
		df1['eDensity{}'.format(t)] = freqList1_n

		mDensity1 = [np.mean(df1.iloc[i].values[2:]) for i in range(len(lst1))]
		mDensity1_reversed = mDensity1[::-1]
		mDensity = 1.0/(binsize*1000)*0.5*(np.array(mDensity1)+np.array(mDensity1_reversed))
	
	df['zPosition'] = lst1
	df['mDensity{}'.format(sigma)] = mDensity
df.to_csv('solvent_df40.csv')
#print(df.head(15))
