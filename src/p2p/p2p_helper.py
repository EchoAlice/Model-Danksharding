from config import ( BIN_DIGITS, 
                     MAX_KEY,
)


# Generate node ids (should be random numbers (0, 2**160 - 1)) to add to routing_table
def generate_node_binary(x):
  node_binary = format(x, '0'+BIN_DIGITS+'b') 
  return node_binary 

def populate_table(routing_table_obj) -> None:
  for i in range(MAX_KEY+1):
    peer_id = generate_node_binary(i)
    if peer_id != routing_table_obj.bin_id:  
      routing_table_obj.add_peer(peer_id)
  return