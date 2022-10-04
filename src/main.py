import time
from helper import ( convert_node_input,
                     convert_string_input,
                     distribute_file_chunks,
                     gather_chunks,
                     points_to_string,
                     reed_solomon_data,         
                     reed_solomon_points,
)


original_blob_data = [1,3,2,1,3,8,1,3,2,1,3,8]                                                          
original_xs = [1,2,3,4,5,6,7,8,9,10,11,12] 
extended_xs = [13,14,15,16,17,18,19,20,21,22,23,24] 
data_chosen = [2, 1, 8, 3, 1, 2798019461, 8, 53738992, 19464695, 1, 5554, 386636]
correlated_xs = [3, 10, 12, 5, 4, 24, 6, 19, 18, 1, 13, 15]

def main():
  # # New version extends DATA and places it within a blob
  # #
  # # ========== 
  # #    NEW  
  # # ========== 

  # extended_data = reed_solomon_data(original_blob_data, original_xs, extended_xs)
  # assert len(extended_data) == len(original_blob_data)


  # # 1. Populate blob with data
  # #
  # # 2. Get nodes to request proofs for individual pieces 
  # # 
  # # 3. Have them gossip their results to one another 


  # derived_data = reed_solomon_data(data_chosen, correlated_xs, original_xs)    
  # assert original_blob_data == derived_data 
  # print("Tah dahhh")
  



  # Old version extends POINTS to storage nodes 
  # 
  # ========== 
  #    OLD        
  # ========== 
  # original_blob_data = [1,3,2,1,3,8,1,3,2,1,3,8]                                                          
  # original_xs = [1,2,3,4,5,6,7,8,9,10,11,12] 
  # extended_xs = [13,14,15,16,17,18,19,20,21,22,23,24] 
  # original_points = [(1, 1), (2, 3), (3, 2), (4, 1), (5, 3), (6,8), (7, 1), (8, 3), (9, 2), (10, 1), (11, 3), (12,8)]

  string = 'ffffffffffffffff'
  # file_chunks = string.encode('ascii')
  original_blob_data = [c for c in string.encode('ascii')] 
  original_xs = list(range(1,len(original_blob_data)+1))           
  extended_xs = list(range(len(original_blob_data)+1, 2*len(original_blob_data)+1))
  original_points = list(zip(original_xs, original_blob_data))


  # Extend data
  extended_points = reed_solomon_points(original_blob_data, original_xs, extended_xs)
  all_points = original_points + extended_points
  assert len(extended_points) == len(original_points)
  
  # =============
  # STORAGE NODES
  # =============
  # 
  # Change the way I use nodes... 
  instantiated_nodes, chunks_per_node = convert_node_input(all_points)
  full_nodes = distribute_file_chunks(instantiated_nodes, all_points, chunks_per_node)
  all_points = 420
  
  # Reconstruct file from any m of n file chunks distributed amongst nodes
  points_for_reconstruction = gather_chunks(full_nodes, original_xs)            # gather chunks doesn't actually need x_original, it just needs the LENGTH of the og data 
  
  # This for loop is necessary bc data stored within nodes are points.
  # Data needs to be stored this way because I'm not keeping track of which node sends
  # me which set of data.
  data_chosen = []
  correlated_xs = []
  for i in range(len(points_for_reconstruction)):
    data_chosen.append(points_for_reconstruction[i][1])
    correlated_xs.append(points_for_reconstruction[i][0])

  original_points_derived = reed_solomon_points(data_chosen, correlated_xs, original_xs)    
  print('original points derived: '+str(original_points_derived))
  assert original_points_derived == original_points 
  print("Tah dahhh")

main()