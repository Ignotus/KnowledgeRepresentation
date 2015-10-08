import os, os.path
import glob
import subprocess
import numpy as np
# simple version for working with CWD

length_of_files = len(glob.glob('sudoku/*'))
times = []
propagations = []
splits = []
for i in range(length_of_files-3):
	subprocess.call(['python main.py MODEL1 "sudoku/test%i.text"'%(i)], shell = True)
	f = open('sudoku/Results/result.txt', 'r')
	time = f.readline()
	times.append(float(time[:-1]))	
	print("time", time[:-1])
	prop = f.readline()
	propagations.append(int(prop[:-1]))
	print("Prop", prop[:-1])
	split = f.readline()
	splits.append(int(split))
	print("Split", split)
	print("index", i)
	
times = np.array(times)
np.save('sudoku/Results/experiment_results_time_all.npy', times)

propagations = np.array(propagations)
np.save('sudoku/Results/experiment_results_propagations_all.npy', propagations)

splits = np.array(splits)
np.save('sudoku/Results/experiment_results_splits_all.npy', splits)


