from config import ( beginning_points,
                     original_file, 
                     x_extension,
                     x_coordinates_for_original_file,
)
from helper import ( create_nodes,
                     distribute_file_chunks,
                     erasure_code,
                     reconstruct_file, 
)

# Create extended points (aka file chunks)
extended_points = erasure_code(beginning_points, x_extension)
points = beginning_points + extended_points

# Create nodes that store file chunks 
empty_nodes = create_nodes() 
full_nodes = distribute_file_chunks(empty_nodes, points)

# Reconstruct file from any m file chunks within nodes
reconstructed_file = reconstruct_file(full_nodes, x_coordinates_for_original_file)

assert reconstructed_file == original_file
print("Tah dahhh")