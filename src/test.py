import pytest
import random
import sympy as sym
from helper import ( distribute_file_chunks, 
                     create_nodes,
                     expand_expression,
                     gather_chunks,
                     lagrange_interpolation,
                     multiply,
                     operate_on_list,
                     one_and_zeros_polynomial,
                     x,
)
# Allias
chunk = list

# CLI command:
# python -m pytest .\src\test.py 
# To see print statements...  python -m pytest -s .\src\test.py 










# ==========================
#  Tests for Lagrange Logic 
# ==========================

@pytest.fixture                             
def x_in_question():
  return 1

@pytest.fixture                             
def points():
  return [[1,1],[2,3],[3,2],[4,1]]

# Make sure y == 1 when evaluated at x_in_question 
def test_one_and_zeros_polynomial(x_in_question, points):
  basic_polynomial = one_and_zeros_polynomial(x_in_question, points)
  expanded_expression = expand_expression(basic_polynomial[0])
  y = expanded_expression.subs({x:x_in_question})/operate_on_list(basic_polynomial[1],multiply)
  
  # Make sure y == 0 when evaluated at all other polynomials 
  sum_all_other_evaluated_polynomials = 0
  for point in points:
    if point[0] != x_in_question: 
      sum_all_other_evaluated_polynomials = sum_all_other_evaluated_polynomials + expanded_expression.subs({x:point[0]})/operate_on_list(basic_polynomial[1],multiply)

  assert y == 1 and sum_all_other_evaluated_polynomials == 0





# ======================
#  Tests for Node Logic
# ======================

# Give nodes full functionality!
#
# Case-
#    string:                Hello
#    x original:          [1,2,3,4,5]
#    extend:                  2
#    nodes:                   5
#    chuncks/node:            2
#    nodes down:     nodes[3], nodes[4]
#
# chunks_gathered = [(7, 141), (2, 101), (5, 111), (1, 72), (6, 122)]
# chunks_off_limits = [(3, 108), (8, 163), (4, 108), (9, 178)]

@pytest.fixture
def x_original():
  return [1,2,3,4,5]

@pytest.fixture
def nodes():
  instantiated_nodes = create_nodes(5)
  all_points = [(1, 72), (2, 101), (3, 108), (4, 108), (5, 111), (6, 122), (7, 141), (8, 163), (9, 178), (10, 171)]
  chunks_per_node = 2 
  distribute_file_chunks(instantiated_nodes, all_points, chunks_per_node)
  mock_downed_nodes(instantiated_nodes)
  return instantiated_nodes 

def mock_downed_nodes(nodes):
  nodes[2].status = False
  nodes[3].status = False
  return 

@pytest.fixture
def chunks_off_limits(nodes) -> list[chunk]:
  chunks_off_limits = []
  for node in nodes:
    if node.status == False: 
      for i in range(len(node.file_chunks)):
        chunks_off_limits.append(node.file_chunks[i])
  return chunks_off_limits

def test_gather_chunks(nodes, x_original, chunks_off_limits):
  chunks_gathered = gather_chunks(nodes, x_original)

  for gathered_chunk in chunks_gathered:
    for off_limit_chunk in chunks_off_limits:
      if off_limit_chunk == gathered_chunk:
        assert False
  assert True