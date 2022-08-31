from config import ( original_points,
                     x_extension,
)
from helper import ( create_nodes,
                     distribute_file_chunks,
                     erasure_encode, 
)


extended_points = erasure_encode(original_points, x_extension)
points = original_points + extended_points
empty_nodes = create_nodes() 
populated_nodes = distribute_file_chunks(empty_nodes, points)

for node in populated_nodes:
  print(node.file_chunks)

# reconstruct_file(nodes)









# Proof of concept:
#
#   - Extended_points created from original points and used to reconstruct the polynomial 
#     used to recover original file 
#
#   - Encorperate node logic

# extended_points = erasure_encode(original_points, x_extension)
# print(extended_points)
# original_points_derived = erasure_encode(extended_points, x_coordinates_for_original_file)

# assert original_points_derived == original_points
# print("Tah dahhh")