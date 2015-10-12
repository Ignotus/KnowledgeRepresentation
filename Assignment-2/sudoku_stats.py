import os, os.path
import glob
import subprocess
import numpy as np
# simple version for working with CWD

# Obtain length of total numbers of sudoku in map sudoku
length_of_files = len(glob.glob('sudoku/*'))

# intialise empty list
times = []
propagations = []
splits = []

# loop over files in sudoku map
for i in range(length_of_files-3):
	# Call solver with variables
	# the solver takes 4 arguments: MODEL1/MODEL2
	#								PROP_ON/PROP_OFF
	#								SPLIT_1/SPLIT_2
	#								filename
	subprocess.call(['python main.py MODEL1 PROP_ON SPLIT_2 "sudoku/test%i.text"'%(i)], shell = True)
	f = open('sudoku/Results/result.txt', 'r')
	# Read results file and put into list
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

# Put results from all sudoku in array.	
times = np.array(times)
np.save('sudoku/Results/experiment_results_time_split2.npy', times)

propagations = np.array(propagations)
np.save('sudoku/Results/experiment_results_propagations_split2.npy', propagations)

splits = np.array(splits)
np.save('sudoku/Results/experiment_results_splits_split2.npy', splits)


