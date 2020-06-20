#Author: SA, June 2020
#this code and finds solvent density autocorrelation 
import numpy as np
import pandas as pd

#get atom_no and starting tim-step
f = open('40sbrush.lammpstrj','r')
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
traj_no = 4000
print(time_step, atom_no)

## read data from different snap-shots separately - tabulate and manipulate the data  
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
	
	lstZ1 = [i[-1] for i in lst if 1<i[1]==7] # all 1 monomers
	lstSorted1 = sorted(lstZ1)
	#print(lstSorted[-1])
	binsize = 10.64/100
	area = 1000
	lst1 = np.arange(0, 10.64+binsize, binsize)
	freqList1 = []
	for i in lst1:
		count = 0
		for j in lstSorted1[sum(freqList1):]:
			if j>=i+binsize:
				break
			count = count+1
		freqList1.append(count)
	#print(freqList)
	freqList1_n = 1.0/binsize*1.0/(area*1)*(np.array(freqList1))
	

	df1['zPosition'] = lst1
	df1['mDensity{}'.format(t)] = freqList1_n #brush1
	
df1.to_csv('df_autocorr.csv') #brush 1

