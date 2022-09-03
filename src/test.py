import pytest
import sympy as sym
from helper import ( x,
                     expand_expression,
                     multiply,
                     operate_on_list,
                     one_and_zeros_polynomial,
)
# CLI command:
# python -m pytest .\src\test_lagrange.py 
# To see print statements...  python -m pytest -s .\src\test_lagrange.py 

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
  y = expanded_expression.subs({x:x_in_question})/operate_on_list(basic_polynomial[1],multiply)
  
  # Make sure y == 0 when evaluated at all other polynomials 
  sum_all_other_evaluated_polynomials = 0
  for point in points:
    if point[0] != x_in_question: 
      sum_all_other_evaluated_polynomials = sum_all_other_evaluated_polynomials + expanded_expression.subs({x:point[0]})/operate_on_list(basic_polynomial[1],multiply)

  assert y == 1 and sum_all_other_evaluated_polynomials == 0


# ==========================
#  Tests for Lagrange Logic 
# ==========================





# ======================
#  Tests for Node Logic
# ======================

# Error messages that have occured within reconstruct_file():
'''
  File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.10_3.10.1776.0_x64__qbz5n2kfra8p0\lib\secrets.py", line 29, in randbelow
    raise ValueError("Upper bound must be positive.")


  File "C:\Users\broycro\Desktop\Programming\erasure-coding\src\helper.py", line 149, in reconstruct_file
    full_nodes.pop(node_in_question.index)
IndexError: pop index out of range
'''