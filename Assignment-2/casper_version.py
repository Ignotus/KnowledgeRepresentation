import sys
import pprint
import numpy as np
import copy
import time

def create_sudoku_matrix(f, size):
  line = f.readline()
  # TODO: Rewrite it for NxN sudoku
  sudoku_matrix = np.zeros((size, size))
  index = 0
  for i in range(size):
    for j in range(size):
      if line[index].isdigit():
        sudoku_matrix[i, j] = line[index]
      else:
        sudoku_matrix[i, j] = 0
      index += 1
  return sudoku_matrix.astype(int)

file_name = 'test.txt'
if len(sys.argv) > 1:
  file_name = sys.argv[1]

sudoku_matrix = create_sudoku_matrix(open(file_name, 'r'), 9)
print(sudoku_matrix)