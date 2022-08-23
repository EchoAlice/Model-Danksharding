import pytest
import sympy as sym
from helper import ( multiply_list,
                     expand_expression,
                     one_and_zeros_polynomial,
                     x,
)
# CLI command:
# python -m pytest .\src\test_lagrange.py 
# To see print statements...  python -m pytest -s .\src\test_lagrange.py 

# Test ones and zeros lagrange.  Make sure that y == 1 when evaluating the polynomial
# at x coordinate in question and y == 0 at all other x coordinates 

@pytest.fixture                             
def x_in_question():
  return 1

@pytest.fixture                             
def points():
  return [[1,1],[2,3],[3,2],[4,1]]

def test_one_and_zeros_polynomial(x_in_question, points):
  # Make sure y == 1 when evaluated at x_in_question 
  basic_polynomial = one_and_zeros_polynomial(x_in_question, points)
  expanded_expression = expand_expression(basic_polynomial[0])
  y = expanded_expression.subs({x:x_in_question})/multiply_list(basic_polynomial[1])
  
  # Make sure y == 0 when evaluated at all other polynomials 
  sum_all_other_evaluated_polynomials = 0
  for point in points:
    if point[0] != x_in_question: 
      sum_all_other_evaluated_polynomials = sum_all_other_evaluated_polynomials + expanded_expression.subs({x:point[0]})/multiply_list(basic_polynomial[1])

  assert y == 1 and sum_all_other_evaluated_polynomials == 0 