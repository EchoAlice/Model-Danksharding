from helper import (create_equations,
                    extrapolate_points,
                    transpose,
)
from itertools import starmap
from copy import copy

file = "1321"
x_coordinates = [1,2,3,4]

# Splits up file 
split_increments = len(x_coordinates) 
file = [int(file[i:i+split_increments]) for i in range(0, len(file), split_increments)]


# Represent formulas as list of coefficients.  Set equation equal to zero
#                        [x_coordinate, y-intercept, y_coordinate]
# Example:  1*a + b - 13 = 0   --> [1,     1,     -13]   
#           2*a + b - 21 = 0   --> [2,     1,     -21]
#
#  We have the coefficients that represent the linear equations, now we need the point to evaluate it at         



# Recursively call this function until there's only one remaining formula.
# Although, I don't think this is really recursion... Definition please  
def linear_system_solve(equations, archive_equations, final_y):
  if len(equations) == 1: 
    # This array keeps track of all values of variables.  When all values are found, unravel_onion will return this full array
    # Does this array need to go inside unravel_onion()? 
    unraveled_onion = []
    final_equation = unravel_onion(archive_equations, unraveled_onion, final_y) 
    print("final_equation: "+str(final_equation)) 
    return final_equation
  
  previous_equation = []
  next_round_of_equations = [[0]*len(equations[0]) for x in range(len(equations)-1)] 
  
  # Subtracts equations from one another, storing next round of equations into seperate array 
  for r in range(len(equations)): 
    current_equation = equations[r]
    if previous_equation: 
      i = r - 1                                   
      for c in range(len(equations[r])): 
        next_round_of_equations[i][c] = current_equation[c] - previous_equation[c]
    previous_equation = current_equation

  # Adds a formula for each round of system solving  (Used to unravel the onion)
  archive_equations.append(next_round_of_equations[0])
  linear_system_solve(next_round_of_equations, archive_equations, final_y)  


# Steps to solve each equation.   Compress this function with recursion 
#
#   1. Transpose y 
#   2. Map each unraveled_onion object with current equation's coefficients 
#   3. Add all known values together 
#   4. Transpose sum
#   5. equation_to_solve[-1] = sum_of_known_values + y
#   6. Divide coefficient for variable in question by right side of equation (equation_to_solve[-1])
#
# Archived equations:    [[7, 3, 1, 0, -2], [12, 2, 0, 0, 3], [6, 0, 0, 0, -3]] 
#
def unravel_onion(archive_equations, unraveled_onion, final_y):
  # Solves for each variable (except for last)
  for i in range(len(archive_equations)):
    equation_to_solve = copy(archive_equations[-1]) 
    equation_to_solve[-1] = transpose(equation_to_solve[-1])
    sum_of_known_values = sum(list(starmap(lambda x,y: x*y, zip(unraveled_onion, archive_equations[-1]))))    
    equation_to_solve[-1] = equation_to_solve[-1] + transpose(sum_of_known_values)
    x = equation_to_solve[-1]/equation_to_solve[i]              
    unraveled_onion.append(x) 
    archive_equations.pop(-1)

  # Solves for last variable. Only works when d's coefficient is 1
  sum_of_known_values = sum(unraveled_onion)
  d = final_y + transpose(sum_of_known_values)
  unraveled_onion.append(d)
  return unraveled_onion


def erasure_encode(file, x_coordinates) -> int:   
  # Should final_y be transposed manually?
  # Or treat it as being on the right side of the equation as-is
  final_y = 1                   
  # to_points(file, x_coordinates) 
  stub = "What info is necessary to create equations of variable size representing polynomials?" 
  equations = create_equations(stub)

  # This value is for "unraveling the onion".  In which function should it be defined?
  archive_equations = [] 
  formula = linear_system_solve(equations, archive_equations, final_y) 
  # extrapolate_points(formula)

erasure_encode(file, x_coordinates)









#  This will be for solving polynomial systems
# def system_solve(equations):
#   # while len(equations) > 1:
#   diff = [] 
#   for i in range(len(equations[0])): 
#     diff.append(equations[0][i] - equations[1][i])

#   # Solves for 'a'           
#   b_plus_y = sum(diff[-2:])
#   x_difference = diff[0] 
#   a = -b_plus_y/x_difference 
  
#   # Solves for 'b' 
#   b = -(equations[0][0]*a + equations[0][-1])
#   print(3.0*a + 5.0*b)
   
#   formula = [a, b]
#   # return formula