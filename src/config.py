import secrets
import sympy as sym
from copy import copy

x = sym.Symbol('x')

# File setup
file = "1321"
file_chunks = [int(c) for c in file]
x_coordinates_for_original_file = [1,2,3,4]  
x_extension = [5,6,7,8]
# x_extension.insert(0,secrets.choice(x_coordinates_for_original_file)) 
original_points = list(zip(x_coordinates_for_original_file, file_chunks))

# Node setup -   These numbers should come from the user's input
number_of_nodes = 5
chunks_per_node = 2
PROBABILITY_NODE_IS_DOWN = 0.1