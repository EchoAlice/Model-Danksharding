import sympy as sym

points = [[1,1],[2,3],[3,2],[4,1]]
x = sym.Symbol('x')

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

lagrange_interpolation(points)