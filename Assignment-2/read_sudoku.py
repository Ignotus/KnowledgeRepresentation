# Reads a large sudoku file and prints all seperate files in map sudoku
import os
f = open('sudoku/sudoku.txt', 'r')

# Obtain ever line in file and put in matrix
index = 1
a = [line for line in f]

# Loop over matrix a
for index, sudoku in enumerate(a):
	# Open location
	location = 'sudoku'
	if not os.path.exists(location):
		os.makedirs(location)
	# Create file name
	filename = "%s/test%i.text" %(location, index)
	# open stream
	a = open(filename, 'w')
	# write to File
	a.write(sudoku)
	a.close()

f.close()