import os, os.path
import glob
import subprocess
import numpy as np
# simple version for working with CWD

length_of_files = len(glob.glob('*'))
times = []
propagations = []

for i in range(length_of_files-6):
	subprocess.call(['python main_print.py "test%i.text"'%(i)], shell = True)
	f = open('Results/result.txt', 'r')
	time = f.readline()
	times.append(float(time[:-1]))	
	print("time", time[:-1])
	
	prop = f.readline()
	propagations.append(int(prop))
	print("Prop", prop)
	print("index", i)
	
times = np.array(times)

np.save('experiment_results_time.npy', times)

propagations = np.array(propagations)
np.save('experiment_results_propagations.npy', propagations)

