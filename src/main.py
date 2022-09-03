from helper import ( create_nodes,
                     convert_input,
                     distribute_file_chunks,
                     erasure_code,
                     reconstruct_file,
)

# Ask user for string to encode and factor to extend data by
beginning_points, string_input, x_original, x_extension  = convert_input() 

# Create extended points (aka file chunks)
extended_points = erasure_code(beginning_points, x_extension)
points = beginning_points + extended_points

# Create nodes that store file chunks 
empty_nodes = create_nodes() 
full_nodes = distribute_file_chunks(empty_nodes, points)

# Reconstruct file from any m file chunks within nodes.  Maybe move randomization logic out here?
reconstructed_file = reconstruct_file(full_nodes, x_original)

assert reconstructed_file == string_input
print("Tah dahhh")