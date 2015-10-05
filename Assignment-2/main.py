import sys
import pprint
import numpy as np
import copy
import time


def create_sudoku_matrix(f):
  line = f.readline()
  sudoku_matrix = np.zeros((9, 9))
  index = 0
  for i in range(9):
    for j in range(9):
      if line[index].isdigit():
        sudoku_matrix[i, j] = line[index]
      else:
        sudoku_matrix[i, j] = 0
      index += 1

  return sudoku_matrix.astype(int)

file_name = 'test.txt'
if len(sys.argv) > 1:
  file_name = sys.argv[1]

sudoku_matrix = create_sudoku_matrix(open(file_name, 'r'))
print(sudoku_matrix)

class Variable:
  def __init__(self):
    self.domain = {}
    self.fixed = False

  def __str__(self):
    return ("Fixed " if self.fixed else "") + str(self.domain)

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
      var = Variable()
      if sudoku[i, j] == 0:
        var.domain = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        var.fixed = False
      else:
        var.domain = {sudoku[i, j]}
        var.fixed = True

      variables[cell_name] = var

      constraints[cell_name] = set()
      for ii in range(row):
        if ii != i:
          constraints[cell_name].add('%d,%d' % (ii, j))

      for jj in range(column):
        if jj != j:
          constraints[cell_name].add('%d,%d' % (i, jj))

      rect_i = (i // 3) * 3
      rect_j = (j // 3) * 3
      for ii in [rect_i, rect_i + 2]:
        for jj in [rect_j, rect_j + 2]:
          constraints[cell_name].add('%d,%d' % (ii, jj))
        
  return variables, constraints

#to_kills = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
#for x, y in to_kills:
#  print('Set %d,%d = %d to 0' % (x, y, sudoku_matrix[x, y]))
#  sudoku_matrix[x, y] = 0
variables, constraints = preprocess_model1(sudoku_matrix)

class Solver:
  def __init__(self, variables, constraints):
    self.variables, self.constraints = variables, constraints
    #sorted_keys = list(self.variables.keys())
    #sorted_keys.sort()
    #print(sorted_keys)
    self.satisfied = False

  def __str__(self):
    string = []
    for variable_name, variable in solver.variables.items():
      #if not variable.fixed:
      string.append(variable_name + ' : ' + str(variable))
    return ', '.join(string)

  def is_happy(self):
    """
        Returns true if a range of each variable has been specified
    """
    for variable in self.variables.values():
      if len(variable.domain) != 1:
        return False
    return True

  def is_unsatisfied(self):
    for key, variable in self.variables.items():
      if len(variable.domain) == 0:
        print('Unsatisfied: len(', key, ') = 0')
        return True
    return False

  def is_atomic(self, variable_domain):
    return len(variable_domain) == 1

  def propagate_fixed_variables(self):
    """
    Propagates fixed variables
    """
    print('Propagating fixed variables...')
    for variable_name, variable in self.variables.items():
      if variable.fixed:
        value = next(iter(variable.domain))
        for constraint in self.constraints[variable_name]:
          if not self.variables[constraint].fixed:
            try:
              self.variables[constraint].domain.remove(value)
            except KeyError:
              pass
    print(self)

    while not self.is_happy():
      new_fixed = []
      for variable_name, variable in self.variables.items():
        if not variable.fixed and len(variable.domain) == 1:
          self.variables[variable_name].fixed = True
          new_fixed.append(variable_name)

      if not new_fixed:
        break
      else:
        print('Propagating more from', new_fixed)
        for variable_name in new_fixed:
          #print('Check', variable_name, self.constraints[variable_name])
          value = next(iter(self.variables[variable_name].domain))
          for constraint in self.constraints[variable_name]:
            if not self.variables[constraint].fixed:
              try:
                #print('Remove', value, 'from domain of', constraint)
                self.variables[constraint].domain.remove(value)
              except KeyError:
                pass


  """
    TODO: Check
  """
  def propagate(self, variable_name, value):
    print('Propagate', variable_name, '=', value)
    new_fixed = []
    for constraint in self.constraints[variable_name]:
      if not self.variables[constraint].fixed:
        try:
          self.variables[constraint].domain.remove(value)
          if len(self.variables[constraint].domain) == 1:
            new_fixed.append(constraint)
        except KeyError:
          pass

    while new_fixed and not self.is_happy():
      print('Propagate deeper')
      new = []
      for variable_name in new_fixed:
        if len(self.variables[variable_name].domain) == 0:
          # Unsatisfied, undo
          return

        value = next(iter(self.variables[variable_name].domain))
        for constraint in self.constraints[variable_name]:
          if not self.variables[constraint].fixed:
            try:
              self.variables[constraint].domain.remove(value)
              if len(self.variables[constraint].domain) == 1:
                new.append(constraint)
            except KeyError:
              pass
      new_fixed = new

  def unpropagate(self, variable_name, prev_state, current_value):
    #for constraint in self.constraints[variable_name]:
    #  if not self.variables[constraint].fixed:
    #    self.variables[constraint].domain.add(prev_state)
    self.variables[variable_name].domain = prev_state
    self.variables[variable_name].domain.remove(current_value)
    print('Unpropagate', variable_name, '=', current_value , '=>', self.variables[variable_name])

  def domain_space_size(self):
    return sum([len(variable.domain) for variable in self.variables.values()])

  def split(self):
    for variable_name, var in self.variables.items():
      if len(var.domain) > 1:
        return variable_name
    # Else -> Sh~~ happens

  def solve(self):
    print(self)
    # Propagates fixed variables
    print('Initial domain size:', self.domain_space_size())
    self.propagate_fixed_variables()
    print('Domain size after fixed variables propagation:', self.domain_space_size())
    if self.is_happy():
      return

    current_variable = self.split()
    domain_state = copy.deepcopy(self.variables[current_variable].domain)
    new_domain = next(iter(domain_state))
    stack = [(current_variable, domain_state, new_domain)];
    print('Setting', current_variable, 'to', {new_domain}, (domain_state))
    self.variables[current_variable].domain = {new_domain}
    while not self.is_happy():
      print('Domain size:', self.domain_space_size())
      #print('Before propagation:', self.variables)
      prev_variable, domain, prev_state = stack[-1]
      undo_state = copy.deepcopy(self.variables)
      #print(self)
      self.propagate(prev_variable, prev_state)
      if self.is_unsatisfied():
        if len(stack) > 0:
          # POP THE STACK!
          print('Unpropagate')

          self.variables = undo_state
          self.unpropagate(prev_variable, domain, prev_state)
          del stack[-1]
          print(self)

      if not self.is_happy():
        #print('I\'m not happy!')
        #if self.is_atomic(variable):
        #  is_continue = False
        #else:
        print('I\'m still not happy! Split more.')
        current_variable = self.split()
        domain_state = copy.deepcopy(self.variables[current_variable].domain)
        new_domain = next(iter(domain_state))
        stack.append((current_variable, domain_state, new_domain))
        print(stack)
        print('Setting', current_variable, 'to', new_domain, (domain_state))
        self.variables[current_variable].domain = {new_domain}
    if self.is_unsatisfied():
      print('Unsatisfied, something weird.')

solver = Solver(variables, constraints)
t1 = time.time()
solver.solve()
print('Consumed time:', (time.time() - t1))
print('Solution:', solver)