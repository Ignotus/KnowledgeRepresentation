# The MIT License (MIT)
#
# Copyright (c) 2015 Minh Ngo
# Copyright (c) 2015 Casper Thuis
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import pprint
import numpy as np
import copy
import time

# Create_sudoku_matrix reads file name and size and return a matrix that contains 
# sudoku and the instanice
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
if len(sys.argv) > 2:
  file_name = sys.argv[2]

sudoku_matrix = create_sudoku_matrix(open(file_name, 'r'), 9)
print(sudoku_matrix)

def preprocess_model1(sudoku):
  """
      Returns variables and constraints
      a variable is a set of its domain
      a constraint is a set of variables that it should not be equal to
  """
  #create variables
  row, column = sudoku.shape
  variables = {}
  constraints = {}
  for i in range(row):
    for j in range(column):
      cell_name = '%d,%d' % (i, j)
      var = None
      if sudoku[i, j] == 0:
        var = {1, 2, 3, 4, 5, 6, 7, 8, 9}
      else:
        var = {sudoku[i, j]}

      variables[cell_name] = var

      cell_constraints = set()
      for ii in range(row):
        if ii != i:
          cell_constraints.add('%d,%d' % (ii, j))

      for jj in range(column):
        if jj != j:
          cell_constraints.add('%d,%d' % (i, jj))

      rect_i = (i // 3) * 3
      rect_j = (j // 3) * 3
      for ii in range(rect_i, rect_i + 3):
        for jj in range(rect_j, rect_j + 3):
          if ii != i and jj != j:
            cell_constraints.add('%d,%d' % (ii, jj))

      constraints[cell_name] = list(cell_constraints)
        
  return variables, constraints

def preprocess_model2(sudoku):
  size, _ = sudoku.shape
  variables = {}
  constraints = {}

  for i in range(size):
    for j in range(size):
      fixedValue = sudoku_matrix[i, j]
      if fixedValue != 0:
        cellName = '%d,%d' % (i, j)
        variables['%d,%dc' % (fixedValue, j)] = {cellName}
        variables['%d,%dr' % (fixedValue, i)] = {cellName}
        boxId = (i // 3) * (size // 3) + j // 3
        variables['%d,%db' % (fixedValue, boxId)] = {cellName}

  for i in range(1, size + 1): # Number
    for j in range(size): # Number index
      varNameC = '%d,%dc' % (i, j)
      varNameR = '%d,%dr' % (i, j)
      varNameB = '%d,%db' % (i, j)
      if varNameC not in variables:
        # j specifies column, k specifies row
        variables[varNameC] = {'%d,%d' % (k, j) for k in range(size)}

      if varNameR not in variables:
        # j specifies row, k specifies column
        variables[varNameR] = {'%d,%d' % (j, k) for k in range(size)}

      if varNameB not in variables:
        # j specifies box
        boxColStart = j * 3 % size
        boxRowStart = (j * 3 // size) * 3
        variables[varNameB] = {'%d,%d' % (m, k) for k in range(boxColStart, boxColStart + 3)
                                                for m in range(boxRowStart, boxRowStart + 3)}
        print(variables[varNameB])

  allConstraints = set(variables.keys())
  print(sorted(list(allConstraints)))
  #sys.exit()
  for i in range(1, size + 1): # Number
    for j in range(size): # Number index
      varNameC = '%d,%dc' % (i, j)
      eqConstraintC = {varNameC}
      # Should be in the j column only
      for k in range(size):
        eqConstraintC.add('%d,%dr' % (i, k))

      for k in range(j // 3, size, 3):
        eqConstraintC.add('%d,%db' % (i, k))

      constraints[varNameC] = list(allConstraints.difference(eqConstraintC))

      varNameR = '%d,%dr' % (i, j)
      eqConstraintR = {varNameR}
      for k in range(size):
        eqConstraintR.add('%d,%dc' % (i, k))

      for k in range((j // 3) * (size // 3), (j // 3) * (size // 3) + 3):
        eqConstraintR.add('%d,%db' % (i, k))

      constraints[varNameR] = list(allConstraints.difference(eqConstraintR))

      varNameB = '%d,%db' % (i, j)
      eqConstraintB = {varNameB}
      boxColStart = (j * 3) % size
      boxRowStart = ((j * 3) // size) * 3
      for k in range(boxRowStart, boxRowStart + 3):
        eqConstraintB.add('%d,%dr' % (i, k))
      for k in range(boxColStart, boxColStart + 3):
        eqConstraintB.add('%d,%dc' % (i, k))
      constraints[varNameB] = list(allConstraints.difference(eqConstraintB))
  return variables, constraints

if sys.argv[1] == 'MODEL1':
  variables, constraints = preprocess_model1(sudoku_matrix)
  #print constraints
elif sys.argv[1] == 'MODEL2':
  variables, constraints = preprocess_model2(sudoku_matrix)
  #print constraints

class Solver:
  def __init__(self, variables, constraints):
    self.variables, self.constraints = variables, constraints

  def __str__(self):
    string = []
    for name, domain in solver.variables.items():
      string.append('%s : %s' % (name, domain))
    return ', '.join(string)

  def is_happy(self):
    """
        Returns true if a range of each variable has been specified
    """
    for domain in self.variables.values():
      if not self.is_atomic(domain):
        return False
    return True

  def is_unsatisfied(self):
    for name, domain in self.variables.items():
      if len(domain) == 0:
        #print('Unsatisfied: len("%s") = 0' % (name))
        return True
    return False

  def is_atomic(self, domain):
    return len(domain) == 1

  def propagate(self):
    print('Propagating')
    newAtomics = []
    for vName, vDomain in self.variables.items():
      if not self.is_atomic(vDomain):
        continue

      vVal = next(iter(vDomain))
      for cName in self.constraints[vName]:
        cDomain = self.variables[cName]
        try:
          cDomain.remove(vVal)
          if self.is_atomic(cDomain):
            newAtomics.append((cName, next(iter(cDomain))))
        except KeyError:
          pass

    while newAtomics:
      ##print('Deeper...', newAtomics)
      atomics = []
      for vName, vVal in newAtomics:
        for cName in self.constraints[vName]:
          cDomain = self.variables[cName]
          try:
            cDomain.remove(vVal)
            if self.is_atomic(cDomain):
              atomics.append((cName, next(iter(cDomain))))
          except KeyError:
            pass
      newAtomics = atomics

  def domain_space_size(self):
    return sum([len(domain) for domain in self.variables.values()])

  def split(self):
    """
    Chooses the variable to split
    """
    smallest_domain_len = 81
    smallest_domain_name = []
    for name in sorted(self.variables.keys()):
      domain = self.variables[name]
      #print ('name', name)      
      #print ('len', len(domain))
      if len(domain) > 1 and smallest_domain_len > len(domain):
        smallest_domain_name = name
        smallest_domain_len = len(domain)
        print('Splitting "%s" with a domain %s' % (name, domain))
    
    return smallest_domain_name


    # Else -> Sh~~ happens

  def solve(self):
    print(self)
    # Propagates fixed variables
    print('Initial domain size:', self.domain_space_size())
    self.propagate()
    print('Domain size after fixed variables propagation:', self.domain_space_size())
    print(self)
    if self.is_happy():
      return

    # DFS stack
    stack = []

    # If we split by a variable A1 and then split by a variable A2, then we don't need
    # to split in the opposite way. Because it's actually the same solution.
    vName = self.split()

    worldState = copy.deepcopy(self.variables)
    # Put each variable in the current_var domain into the stack
    for val in sorted(list(self.variables[vName])):
      stack.append((vName, val, worldState))

    decisionStack = []
    while stack and not self.is_happy():
      print('Decision stack:', [(vName, val) for vName, val, _ in decisionStack])
      print('Stack:', [(vName, val) for vName, val, _ in stack])
      vName, val, worldState = stack.pop()
      self.variables[vName] = {val}
      #print('Setting "%s" to %d' % (vName, val))
      ##print('In the stack:', [(vName, val) for vName, val, _ in stack[-5:]])
      decisionStack.append((vName, val, worldState))
      ##print('In the decision stack:', [(vName, val) for vName, val, _ in decisionStack[-5:]])
      self.propagate()

      # If it's unsatisfied solution. Then we need to backtrack.
      if self.is_unsatisfied():
        # If it's the last child then pop a parent (because a parent
        # is not satisfied as well).
        print('Unpropagate')
        vName, _, undoState = decisionStack.pop()
        while stack and decisionStack and (stack[-1][0] != vName):
          vName, _, undoState = decisionStack.pop()
          #print('Unpropagate to the parent %s' % (vName))
        self.variables = copy.deepcopy(undoState)
      elif not self.is_happy():
        vName = self.split()
        worldState = copy.deepcopy(self.variables)
        for val in sorted(self.variables[vName]):
          stack.append((vName, val, worldState))

solver = Solver(variables, constraints)
t1 = time.time()
solver.solve()
print('Consumed time:', (time.time() - t1))
print('Solution:', solver)

def fill_sudoku_model1(sudoku, solution):
  for i in range(sudoku.shape[0]):
    for j in range(sudoku.shape[1]):
      if sudoku[i, j] == 0:
        sudoku[i, j] = next(iter(solution['%d,%d' % (i, j)]))

print(solver.domain_space_size())
if sys.argv[1] == 'MODEL1':
  fill_sudoku_model1(sudoku_matrix, solver.variables)
print(sudoku_matrix)