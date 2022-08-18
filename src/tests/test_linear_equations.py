import pytest
import numpy as np
# import sys
# sys.path.append("..")
from .. import main                                      # Same bug where I need to use sys
from main import linear_system_solve
#  Create a class for each type of test.


# =============================
# Tests for linear system solve 
# =============================
equations= [[1, 1, 1, 1, -1],
            [8, 4, 2, 1, -3],
            [27, 9, 3, 1, -2],
            [64, 16, 4, 1, -1]]                 


correct_formula = [6, 5, 5]

@pytest.fixture
def input_values():
  equations= [[1, 1, -13],
              [2, 1, -21],        # 1, 0, -8
              [7, 5, -3]]         # 6, 5, 5
  return equations

def test_first_coefficient_solver(input_values):
  assert linear_system_solve(input_values) == correct_formula


# ================================
# Create tests for unraveled onion
# ================================

[[7, 3, 1, 0, -2], [12, 2, 0, 0, 3], [6, 0, 0, 0, -3]]
