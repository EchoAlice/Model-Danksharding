from itertools import starmap
from copy import copy

def transpose(x):
  return -x

def create_equations(file_chunks): 
  num_of_equations = len(file_chunks)
  length_of_equation = len(file_chunks) + 1 

  equations = []                                                  
  for r in range(num_of_equations):    
    equation = [] 
    degree = num_of_equations - 1 
    for c in range(length_of_equation):
      if c == range(length_of_equation)[-1]: 
        equation.append(transpose(file_chunks[r])) 
      else:
        coefficient = ((r+1)**degree) 
        equation.append(coefficient) 
        degree = degree-1 
    equations.append(equation) 
  return equations

# Recursively call this function until there's only one remaining formula.
def system_solve(equations, archive_equations, final_y):
  previous_equation = []
  next_round_of_equations = [[0]*len(equations[0]) for x in range(len(equations)-1)] 
  
  if len(equations) == 1: 
    final_equation = unravel_onion(archive_equations, final_y) 
    return final_equation
  
  else:  
    # Subtracts equations from one another, storing next round of equations into seperate array 
    for r in range(len(equations)): 
      i = r - 1                                   
      if previous_equation: 
        for c in range(len(equations[r])): 
          next_round_of_equations[i][c] = equations[r][c] - previous_equation[c]
      previous_equation = equations[r]

    # Adds a formula for each round of system solving  (Used to unravel the onion)
    archive_equations.append(next_round_of_equations[0])
    system_solve(next_round_of_equations, archive_equations, final_y)  
  
# Steps to solve each equation: 
#   1. Transpose y 
#   2. Map each unraveled_onion object with current equation's coefficients 
#   3. Add all known values together 
#   4. Transpose sum
#   5. equation_to_solve[-1] = sum_of_known_values + y
#   6. Divide coefficient for variable in question by right side of equation (equation_to_solve[-1])
#
# Archived equations:    [[7, 3, 1, 0, -2], [12, 2, 0, 0, 3], [6, 0, 0, 0, -3]] 
#
def unravel_onion(archive_equations, final_y):
  unraveled_onion = [] 
  # Solves for each variable (except for last)
  for i in range(len(archive_equations)):
    equation_to_solve = copy(archive_equations[-1]) 
    equation_to_solve[-1] = transpose(equation_to_solve[-1])
    sum_of_known_values = sum(list(starmap(lambda x,y: x*y, zip(unraveled_onion, archive_equations[-1]))))    
    equation_to_solve[-1] = equation_to_solve[-1] + transpose(sum_of_known_values)
    x = equation_to_solve[-1]/equation_to_solve[i]              
    unraveled_onion.append(x) 
    archive_equations.pop(-1)

  # Solves for last variable. Is d's last variable always 1?
  sum_of_known_values = sum(unraveled_onion)
  d = final_y + transpose(sum_of_known_values)
  unraveled_onion.append(d)
  return unraveled_onion

def extrapolate_points(polynomial, x_coordinates):
  extended_file_chunks = [] 
  for x_coordinate in x_coordinates:
    extended_file_chunks.append(evaluate_polynomial(polynomial, x_coordinate))
  return extended_file_chunks 

def evaluate_polynomial(polynomial, x_coordinate):
  sum = 0 
  power = len(polynomial) - 1 
  for coefficient in polynomial:
    operation = coefficient*(x_coordinate)**power 
    sum = sum + operation 
    power = power - 1
  return sum 