import sympy as sym
x = sym.Symbol('x')

def transpose(num):
  return -num

def expand_expression(list_of_expressions):
  expanded_expression = list_of_expressions[0] 
  for i in range(len(list_of_expressions)-1):
    expanded_expression = sym.expand(expanded_expression*list_of_expressions[i+1])
  return expanded_expression

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

def multiply_list(list):
  if len(list) == 1:
    return list[0]
  else:
    list[-2] = list[-1]*list[-2]
    list.pop(-1)
    return multiply_list(list)

# Lagrange
def lagrange_interpolation(points):
  polynomials = [] 
  for point in points:
    polynomials.append(one_and_zeros_polynomial(point[0], points))  
  print(polynomials)
  return "final polynomial" 

def one_and_zeros_polynomial(x_in_question, points):
  basic_polynomial = []
  for i in range(2):
    half_poly = []
    for point in points:
      if x_in_question != point[0] and i == 0:
        half_poly.append((x - point[0]))  
      if x_in_question != point[0] and i == 1:
        half_poly.append((x_in_question - point[0]))
    basic_polynomial.append(half_poly) 

  return basic_polynomial


def reconstruct_original_file():
  return