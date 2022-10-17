from config import ( BIN_DIGITS, 
                     BIN_MAX_KEY,
                     k,
                     MAX_KEY,
)
from p2p_helper import ( populate_table, 
                         generate_node_binary,
)

# ==============================
#  Create Routing table
# ==============================
#
#    To Do:
#    - Make distance metric to know which peer is responsible for which keys  
#    - Which of my nodes is closest without going over this key? 
#    - (Refer to Kademlia video)
#
#
#    To Do (L8r):
#    - Create node data type.  What info ABOUT a node needs to be stored? 
#    - Create delete (and replace?) function(s)
#    - Encorperate node ids with keyspace 2**160


class RoutingTable:
  def __init__(self, bin_id): 
    self.bin_id = bin_id 
    self.table = [[-1]*k for _ in BIN_MAX_KEY]                  

  def add_peer(self, peer_id) -> None: 
    if self.contains(peer_id) == True:
      return      
    row_index = self.find_row(peer_id)

    self.place_inside_bucket(peer_id, self.table[row_index]) 
    return

  # Add functionality of bucket being a linked list and updates peers! 
  # Organized:   oldest peer -> youngest peer 
  def place_inside_bucket(self, peer_id, layer) -> None:
    for i in range(k):  
      if layer[i] == -1: 
        layer[i] = peer_id
        return 
    return

  # Maybe contains should return row and column for the node id
  def contains(self, peer_id):
    row_index = self.find_row(peer_id)
    for i in range(k):
      if peer_id == self.table[row_index][i]:
        return True   
    return False

  def find_row(self, peer_id) -> int:
    for i in reversed(range(len(BIN_MAX_KEY))): 
      if peer_id[:i] == self.bin_id[:i]:
        return i
  
  def remove(self):
    pass




# (key, value) pairs are stored on nodes with IDs 'close' to the key
#
#  HashTable needs to keep up with source node's closest k nodes
class HashTable:
  
  def __init__(self, bin_id):
    self.bin_id = bin_id
    self.table = self.calc_range()

  def calc_hash(value: int) -> int:
    key = 'dummy'

    return key
  




# =============================
#  Initialize Routing Table(s)
# =============================
source_node = generate_node_binary(4) 
routing_table = RoutingTable(source_node)
populate_table(routing_table)

# Initializes set of routing tables.
tables = []
for i in range(MAX_KEY+1):
  binary_i = generate_node_binary(i) 
  new_table = RoutingTable(binary_i) 
  populate_table(new_table) 
  tables.append(new_table)
