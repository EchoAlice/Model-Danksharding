import sympy as sym

x = sym.Symbol('x')

# Turn these variables into user generated, CLI inputs 

# File setup
original_file = "1321"
file_chunks = [int(c) for c in original_file]
x_coordinates_for_original_file = [1,2,3,4]  
x_extension = [5,6,7,8]
beginning_points = list(zip(x_coordinates_for_original_file, file_chunks))

# Node setup -   These numbers should come from the user's input
number_of_nodes = 5
chunks_per_node = 2
probability_node_is_down = 0.1