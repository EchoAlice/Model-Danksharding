import sympy as sym
x = sym.Symbol('x')

def add(a,b):
  return a+b 

def multiply(a,b):
  return a*b

def transpose(num):
  return -num

def expand_expression(list_of_expressions):
  expanded_expression = list_of_expressions[0] 
  for i in range(len(list_of_expressions)-1):
    expanded_expression = sym.expand(expanded_expression*list_of_expressions[i+1])
  return expanded_expression

def operate_on_list(list, operation):
  if len(list) == 1:
    return list[0]
  else:
    list[-2] = operation(list[-1],list[-2])
    list.pop(-1)
    return operate_on_list(list, operation)

# ========
# Lagrange
# ========
def lagrange_interpolation(points):
  polynomials = []
  final_form_polynomials = [] 
  for i in range(len(points)):
    polynomials.append(one_and_zeros_polynomial(points[i][0], points))  
    final_form_polynomials.append(points[i][1]*expand_expression(polynomials[i][0])/operate_on_list(polynomials[i][1], multiply))
  final_polynomial = operate_on_list(final_form_polynomials, add)
  return final_polynomial 

def one_and_zeros_polynomial(x_in_question, points):
  basic_polynomial = []
  for i in range(2):
    half_poly = []
    for point in points:
      if x_in_question != point[0]:
        if i == 0:
          half_poly.append((x - point[0]))  
        if i == 1:
          half_poly.append((x_in_question - point[0]))
    basic_polynomial.append(half_poly) 
  return basic_polynomial

def extrapolate_points(polynomial, x_coordinates):
  # Should I create points (x and y) or file chunks (just y) 
  extended_file_chunks = [] 
  for x_coordinate in x_coordinates: 
    y = polynomial.subs({x:x_coordinate})
    extended_file_chunks.append(y)
  return extended_file_chunks 