import copy
from p2p_helper import generate_node_binary, populate_table
from config import ( k, 
                     MAX_KEY,
)

# =========
# TREE NODE
# =========
#
# This will keep track of positions within the tree.
#
# TREE NODES ALWAYS START OUT AS A BUCKET CARRYING NODE
class TreeNode:
  def __init__(self, prefix):
    self.prefix = prefix 
    self.left = None
    self.right = None
    self.bucket = Bucket(prefix) 

  # If a tree node doesn't have any children, THEN a bucket must exist at that tree node's position
  def add_bucket(self):
    if self.left== None and self.right == None: 
      self.bucket = Bucket(self.prefix_bit)
    return 


# ======
# Bucket 
# ======
#
# The common prefix is its position in the tree.
class Bucket:
  bucket_length = k

  # if the prefix changes, the bucket's range is NOT automatically changed  
  def __init__(self, prefix):  
    self.prefix = prefix
    self.bucket_range = self.bucket_range(prefix)        # Figure this one out! Might not need this attribute 
    self.peer_ids = [-1]*k

  # This function works 
  def add_peer(self, peer):
    first_empty_index = None 

    for i in range(len(self.peer_ids)):
      if self.peer_ids[i] == peer:
        print('Peer is already inside of bucket')  
        return
      if self.peer_ids[i] == -1 and first_empty_index == None:
        first_empty_index = i
    if first_empty_index == None:
      return 'Full'
    self.peer_ids[first_empty_index] = peer  
    return


  def delete_peer(self):
    return 


  def bucket_range(self, prefix) -> list:
    bucket_range = [] 
    
    if prefix == None:
      bucket_range = [0, MAX_KEY] 
      return bucket_range
    # How do i calculate the bucket's range?




# =============
# Routing Table
# =============
#
class RoutingTable:
  root = TreeNode(None)      # Maybe place TreeNode(None) in self.table, and change self.table to self.root

  def __init__(self, bin_id): 
    self.bin_id = bin_id 
    self.table = self.root                  
    self.depth = 0     # <---- Same as the number of prefix bits that match source node.  When i add a bucket, add to the max depth 

  def add_peer(self, peer) -> None:
    source = self.bin_id 
    root = self.table  
    path = self.find_path(peer)                
    tree_node = self.traverse(root, path)
    add_peer_result = tree_node.bucket.add_peer(peer)

    # If full, check to see if it's at the closest bucket 
    if add_peer_result == 'Full':
      if path == None or tree_node.prefix[:self.depth] == source[:self.depth]:         
        peers = copy.deepcopy(tree_node.bucket.peer_ids) 
        peers.append(peer)
        self.split_closest_k_bucket(path, tree_node, peers)            

    self.bredth_first_search(root)
    return


  # If the k-bucket's range includes u's own node ID, then the bucket is split into two new 
  # buckets, the old contents divided between the two, and the insertion attempt repeated  
  def split_closest_k_bucket(self, path, parent_node, peers) -> None:
    bit_matching_index = self.depth 
    closest_prefix_bit = self.bin_id[bit_matching_index]
     
    # CREATE NEW BUCKETS
    if path == None:
      left_prefix = '0'
      right_prefix = '1' 
    else:
      left_prefix = path + '0'
      right_prefix = path + '1' 

    # Create new left and right nodes, and remove original bucket
    parent_node.left = TreeNode(left_prefix)
    parent_node.right = TreeNode(right_prefix) 
    parent_node.bucket = None

    # MOVE PEERS TO NEW BUCKETS
    new_closest_bucket, new_sister_bucket = self.new_buckets(closest_prefix_bit, parent_node) 
    
    # Keep track of peers that have been added to new buckets. 
    # If closest K bucket is STILL full, just returns without placing the last peer 
    for peer in peers:
      if peer[bit_matching_index] == closest_prefix_bit:
        new_closest_bucket.add_peer(peer)   
      else:  
        new_sister_bucket.add_peer(peer) 

    self.depth += 1 
    return


  # Allows us to visualize the routing table
  def bredth_first_search(self, root) -> None:
    queue = []
    queue.append(root)

    if root.left == None and root.right == None:
      return 

    print('\n')
    print('Routing Table:')
    print('-------------------------------------')
    while queue:
      queue_buckets = []
      children = [] 
      # For each item in level, add children (if present) to children array
      for i in range(len(queue)):
        if queue[i].bucket != None:
          queue_buckets.append((queue[i].prefix, queue[i].bucket.peer_ids)) 
        if queue[i].left != None: 
          children.append(queue[i].left) 
        if queue[i].right != None:
          children.append(queue[i].right) 

      # Print second closest nodes, then closest nodes.  Separate the two buckets 
      if len(queue_buckets) > 0: 
        print(queue_buckets)
      
      queue = children
    return


  # Follow the path from root down to the correct node 
  def traverse(self, root, path) -> TreeNode:
    tree_node = root 

    # At root node. No buckets have split
    if path == None:
      return tree_node
    
    for bit in path:
      if bit == '0':
        tree_node = tree_node.left 
      if bit == '1':
        tree_node = tree_node.right 
    return tree_node
  
  
  # ----------------
  # Helper functions
  # ----------------

  # Finds correct path to tree node in order to place peer inside of its bucket 
  def find_path(self, peer) -> str:
    prefix = []
    source = self.bin_id 
    distance = self.xor_distance(peer, source)
    
    # ------------ 
    #  Edge cases  
    # ------------ 
    # At root node.  Change this to... 
    if self.table.left == None and self.table.right == None: 
      return None
    # No common path.  Return opposite node from first bit 
    if distance[0] == '1': 
      if self.bin_id[0] == '0':
        return '1' 
      return '0'

    # This loop should only be cycled through as long as it hasn't surpassed the maximum depth 
    print('depth of tree: '+str(self.depth)) 
    for i in range(self.depth):
      if distance[i] == '0': 
        prefix.append(source[i])
      # Provides an off ramp for peers that should be placed in intermediate buckets.
      else:
        prefix.append(peer[i]) 
        break
    
    print('Path to peer: '+str(''.join(prefix)))
    return ''.join(prefix)

  def xor_distance(self, s1, s2) -> str:
    xor_list = [str(ord(a) ^ ord(b)) for a,b in zip(s1,s2)]
    xor_diff = ''.join(xor_list)
    return xor_diff
  
  def new_buckets(self, bit, parent_node) -> list[TreeNode]:
    if bit == '0':
      return parent_node.left.bucket, parent_node.right.bucket 
    return parent_node.right.bucket, parent_node.left.bucket



# ========================
#  Populate Routing Table
# ========================
source_node = generate_node_binary(4)
routing_table = RoutingTable(source_node)

for i in range(MAX_KEY+1):
  peer_id = generate_node_binary(i)
  if peer_id != source_node:  
    print('\n')
    print('\n') 
    print("i: "+str(i)) 
    print('Peer: '+str(peer_id)) 
    routing_table.add_peer(peer_id)
