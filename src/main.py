import time
from helper import ( convert_node_input,
                     convert_string_input,
                     distribute_file_chunks,
                     erasure_code,
                     gather_chunks,
                     points_to_string,
)

# start_time = time.time()
# main() 
# print('Run time: ')
# print("--- %s seconds ---" % (time.time() - start_time))
# print('\n')

# string_input = 'ffffffffffffffff'
# string_input = 'ffffffffffffffffffffffffffffffff'                    
# string_input = 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff'                    

def main():
  # Convert input to points 
  # string_input = input('Enter string to encode: ')                    
  # string_input = '1321'
  # beginning_points, x_original, x_extension  = convert_string_input(string_input) 

  string_input = 1321
  beginning_points = [(1, 1), (2, 3), (3, 2), (4, 1)]
  x_original = [1,2,3,4] 
  x_extension = [5,6,7,8] 

  # Extend data
  extended_points = erasure_code(beginning_points, x_extension)
  print(extended_points) 
  all_points = beginning_points + extended_points

  # Distribute data amongst nodes and wipe out local memory of points
  instantiated_nodes, chunks_per_node = convert_node_input(all_points)
  full_nodes = distribute_file_chunks(instantiated_nodes, all_points, chunks_per_node)
  all_points = 420

  # Reconstruct file from any m of n file chunks distributed amongst nodes
  points_for_reconstruction = gather_chunks(full_nodes, x_original)            # gather chunks doesn't actually need x_original, it just needs the LENGTH of the og data 
  original_points = erasure_code(points_for_reconstruction, x_original)    
  # reconstructed_string = points_to_string(original_points) 
  # assert reconstructed_string == string_input

  assert original_points == beginning_points 
  print("Tah dahhh")

main()