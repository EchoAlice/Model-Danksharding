import pytest
import numpy as np
from main import ( linear_system_solve,
                   file_chunks,
)
from helper import create_equations

#  Create a class for each type of test.



# =============================
# Tests for create_equations() 
# =============================
# def test_create_equations():
#   assert create_equations() == [0.5, -4.5, 12.0, -7.0]

# =============================
# Tests for linear_system_solve 
# =============================
file_chunks
@pytest.fixture                             #  Make test that ensures each value is a square, instead of hard coding correct equation
def system_solve_input():
  equations= [[1, 1, 1, 1, -1],
              [8, 4, 2, 1, -3],
              [27, 9, 3, 1, -2],
              [64, 16, 4, 1, -1]],
  archived_equations = [],
  final_y = 1               
  return equations, archived_equations, final_y 

@pytest.fixture                             #  Make test that ensures each value is a square, instead of hard coding correct equation
def input_values():
  equations= [[1, 1, 1, 1, -1],
              [8, 4, 2, 1, -3],
              [27, 9, 3, 1, -2],
              [64, 16, 4, 1, -1]]                 
  return equations

def test_linear_system_solve():
  assert linear_system_solve( [[1, 1, 1, 1, -1],
                               [8, 4, 2, 1, -3],
                               [27, 9, 3, 1, -2],
                               [64, 16, 4, 1, -1]],
                              [],
                              1 
  ) == [0.5, -4.5, 12.0, -7.0]



# ================================
# Create tests for unraveled onion
# ================================
