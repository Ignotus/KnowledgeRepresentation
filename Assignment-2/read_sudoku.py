import os
f = open('sudoku/sudoku.txt', 'r')

index = 1
a = [line for line in f]
print a

for index, sudoku in enumerate(a):
	print len(sudoku)
	location = 'sudoku'
	filename = "%s/test%i.text" %(location, index)
	a = open(filename, 'w')
	a.write(sudoku)
	a.close()

f.close()