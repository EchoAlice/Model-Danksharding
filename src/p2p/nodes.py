from dht import PeerNode, RoutingTable #,HashTable
from blob import samples
from config import ( MAX_BIN_DIGITS, 
                     MAX_KEY,
)
from p2p_helper import ( generate_node_binary,
                         generate_random_bitstring, 
                         populate_table,
)

'''
  Now that I'm mocking DAS blob interaction,  nodes should be requesting 
  individual samples (and proofs) from the proposer, and telling others within
  the network if they've validated their share, instead of storing data themselves.


  Assumptions:
    1. All nodes are only focused on indexing one blob's samples 
    2. Each node is responsible for knowing about the status of a few samples within this blob.
    3. A node is already aware of vertical subnets. We aren't recreating this process 
    4. A node's chunks (vertical subnet aggregation attestations) are correct
    5. All nodes stay up all the time (nodes don't have to ping or replace peers once they're inside of routing table)
    6. No latency sensitive routing for now. (Don't worry about node's distance from each other IRL)
'''


# Node info = {IP address, UDP port, node id}
#
#       - IP address     ()    
#       - UDP port       (16 bits)
#       - NodeID         160 bit int
#
#       - Key            160 bit int (typically hash of a string key)
#       - Value          Byte array (fits in udp packet?)
#       - Nonce          160 bit int.  Not sure what this is for

# Contains all information, and RPCs
class Node:
  def __init__(self, node_id):
    self.node_id = node_id                           
    self.ip_address = None 
    self.udp_port = None 
    self.routing_table = RoutingTable(node_id)  
    # self.hash_table = HashTable(node_id)                  
    # self.closest_nodes_info =  This could be useful for fast lookup times when a peer node wants info from you!

  def find_value(self, key: int) :
    # while:   
    #   if key is within the node's keyspace   ~this_node < key < next node~    search its hash table:
    #     routing_table.contains()
    #     return value  
    #   else:
    #     closest_k_nodes = peer_node.find_nodes()     ~ node id < key ~ 
    #     do something with closest_k_nodes!!!  
    # return value
    pass 
  
  def find_nodes(self, key: int) -> int:
    # Give user closest ROW of nodes you have to the key 
    # self.routing_table 
    pass
  
  def get(key: int):
    pass

  # (key, value)
  def store(self):
    pass


# ------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------



# =====================================
# Populate node(s) with Routing Tables!
# =====================================

# source_node_id = 
source_node = Node(generate_node_binary(4))
# routing_table = RoutingTable(source_node.node_id)







# ================================
# Populate RT with PeerNode class!
# ================================
for i in range(MAX_KEY+1):
  peer_to_add = PeerNode(generate_random_bitstring(MAX_KEY, MAX_BIN_DIGITS)) 
  source_node.routing_table.add_peer(peer_to_add)
  print('\n') 
  print('===========================================================================') 
  print('New Peer: '+str(peer_to_add.node_id)) 
  print('===========================================================================') 
  if i == 3:
    peer_to_find = peer_to_add
    print('Peer to find: '+str(peer_to_find.node_id))

# Find Peer within table
#------------------------
print('Peer to find: '+str(peer_to_find.node_id))
node_id = peer_to_find.node_id
peer_node = source_node.routing_table.search(node_id)
if peer_node != None:
  print('Peer found: '+str(peer_node.node_id))
else:
  print('Peer not found')

# Delete Peer within table
#--------------------------
print('\n')
print('Delete peer') 
source_node.routing_table.delete_peer(node_id)

# View source node's final table
#--------------------------------
print('\n')
print('Source Node')
print('ID: '+str(source_node.node_id))
print('Routing Table: '+str(source_node.routing_table.bredth_first_search(source_node.routing_table.root)))



# ======================== 
# Encorperate Blob Objects 
# ======================== 