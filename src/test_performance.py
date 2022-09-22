from copy import copy
from main import main
import time
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
# CLI command:
# python -m pytest .\src\test.py 
# To see print statements...  python -m pytest -s .\src\test.py 



# ==================
#  Test Performance 
# ==================

# 32 byte string
@pytest.fixture                             
def byte_string():
  string = 'f'
  for i in range(31):
    string = string + 'f'
  return string 

def test_main():
  return main()


#  Rinkadink test
start_time = time.time()
main()

print('Total test time')
print("--- %s seconds ---" % (time.time() - start_time))