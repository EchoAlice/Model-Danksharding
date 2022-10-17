from dht import RoutingTable, HashTable
from config import ( samples,
)
from p2p_helper import ( generate_node_binary,
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
    5. All nodes stay up all the time (nodes don't have to ping)
    6. No latency sensitive routing for now. (Don't worry about node's distance from each other IRL)
'''

class Blob:
  def __init__(self, samples): 
    self.samples = samples 

# Node info = {IP address, UDP port, node id}
#       - IP address
#       - UDP port
#       - Node ID 

class Node:
  def __init__(self, bin_id):
    self.bin_id = bin_id                           
    self.routing_table = RoutingTable(bin_id)  
    self.hash_table = HashTable(bin_id)                  
  
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

  def put():
    pass

  # (key, value)
  def store(self):
    pass





# ===================== 
#  Instantiate objects
# ===================== 
blob = Blob(samples)
node = Node(generate_node_binary(4))


populate_table(node.routing_table)
# Check out the node's routing table!
print(node.routing_table.bin_id)
print(node.routing_table.table)