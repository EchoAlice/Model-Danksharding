import pytest
import sympy as sym
from helper import multiply_list
x = sym.Symbol('x')
# CLI command:
# python -m pytest .\src\test_lagrange.py 
# To see print statements...  python -m pytest -s .\src\test_lagrange.py 

# Test ones and zeros lagrange.  Make sure that y == 1 when evaluating the polynomial
# at x coordinate in question and y == 0 at all other x coordinates 

@pytest.fixture                             
def x_in_question():
  return 4

@pytest.fixture                             
def points():
  return [[1,1],[2,3],[3,2],[4,1]]

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


def test_one_and_zeros_polynomial(x_in_question, points):
  basic_polynomial = one_and_zeros_polynomial(x_in_question, points)
  expand_expression = basic_polynomial[0][0] 
  for i in range(len(basic_polynomial[0])-1):
    expand_expression = sym.expand(expand_expression*basic_polynomial[0][i+1]) 
  numerator =  expand_expression.subs({x:x_in_question})
  print("numerator: "+str(numerator)) 
  denominator = multiply_list(basic_polynomial[1]) 
  print("denominator: "+str(denominator)) 
  y = numerator/denominator
  
  assert y == 1 