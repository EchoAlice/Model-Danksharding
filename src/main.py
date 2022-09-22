from helper import ( convert_node_input,
                     convert_string_input,
                     distribute_file_chunks,
                     erasure_code,
                     gather_chunks,
                     points_to_string,
)

def main():
  

  # Ask user for string to encode
  beginning_points, string_input, x_original, x_extension  = convert_string_input() 

  # Extend data
  extended_points = erasure_code(beginning_points, x_extension)
  all_points = beginning_points + extended_points
  print('all_points: '+str(all_points))

  # Distribute data amongst nodes and wipe out local memory of points
  instantiated_nodes, chunks_per_node = convert_node_input(all_points)
  full_nodes = distribute_file_chunks(instantiated_nodes, all_points, chunks_per_node)
  all_points = 420

  # Reconstruct file from any m of n file chunks distributed amongst nodes
  points_for_reconstruction = gather_chunks(full_nodes, x_original)            # gather chunks doesn't actually need x_original, it just needs the LENGTH of the og data 
  original_points = erasure_code(points_for_reconstruction, x_original)    
  reconstructed_string = points_to_string(original_points) 

  assert reconstructed_string == string_input
  print("Tah dahhh")

# main()