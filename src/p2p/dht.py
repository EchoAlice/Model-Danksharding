import copy
from tkinter.tix import Tree
from p2p_helper import ( generate_node_binary, 
                         generate_random_bitstring,
)
from config import ( k, 
                     MAX_BIN_DIGITS,
                     MAX_KEY,
)

#                   \\\\\\\\\\\\\\\///////////////
#                    ============================
#                        Create Routing Table
#                    ============================
#                   ///////////////\\\\\\\\\\\\\\\
#
#    To Do:
#    - Create HashTable 
#    - Encorperate node ids with keyspace 2**160


# ==============
# Helper Classes 
# ==============
#
# Contains a subset of Node info that a node's routing table must store
class PeerNode:
  def __init__(self, node_id: str):  
    self.node_id = node_id               
    self.ip_address = None 
    self.udp_port = None 

# Keeps track of positions within the tree.
class TreeNode:
  def __init__(self, prefix: str):
    self.prefix = prefix 
    self.left = None
    self.right = None
    self.bucket = Bucket(prefix) 
  
  def delete_bucket(self):
    self.bucket = None 
    return

# The common prefix is its position in the tree.  Later: Add linked list functionality 
class Bucket:
  def __init__(self, prefix: str):  
    self.prefix = prefix
    self.peers = [-1]*k

  def add_peer(self, peer: PeerNode):
    if self.search(peer.node_id) != None: 
      print('Peer is already here') 
      return 
    # Cycle through bucket until you find an empty spot
    for i in range(len(self.peers)):
      if self.peers[i] == -1:
        self.peers[i] = peer
        return
    return 'Full'

  # Can't recycle search() for delete_peer() without increasing complexity 
  def delete_peer(self, node_id: str):
    for i in range(len(self.peers)): 
      if self.peers[i] != -1: 
        if self.peers[i].node_id == node_id: 
          self.peers[i] = -1
          return 
    print('Peer is not here') 
    return

  def search(self, node_id: str) -> PeerNode:     
    for i in range(len(self.peers)):
      if self.peers[i] != -1:
        if self.peers[i].node_id == node_id:
          return self.peers[i] 
    return 




# =============
# Routing Table
# =============
#
class RoutingTable:
  def __init__(self, source_id: str): 
    self.source_id = source_id 
    self.root = TreeNode(None)                  
    self.depth = 0       # Prefix bits <= depth 

  def add_peer(self, peer: PeerNode) -> None:
    tree_node, path = self.traverse(peer.node_id) 
    add_peer_result = tree_node.bucket.add_peer(peer)
    if add_peer_result == 'Full':
      # Check to see if full bucket is at the closest bucket 
      if path == None or tree_node.prefix[:self.depth] == self.source_id[:self.depth]:                           
        peers = copy.deepcopy(tree_node.bucket.peers) 
        peers.append(peer)
        self.split_closest_k_bucket(path, tree_node, peers)            
    self.bredth_first_search(self.root)
    return

  # Only focus on removing peer for now.  Don't worry about deleting a bucket completely.
  # Should take in a node id as its argument
  def delete_peer(self, node_id: str):
    tree_node, path = self.traverse(node_id) 
    tree_node.bucket.delete_peer(node_id) 
    return

  # If the k-bucket's range includes u's own node ID, then the bucket is split into two new 
  # buckets, the old contents divided between the two, and the insertion attempt repeated  
  def split_closest_k_bucket(self, path: str, parent_node: TreeNode, peers: list[PeerNode]) -> None:
    bit_matching_index = self.depth 
    closest_prefix_bit = self.source_id[bit_matching_index]
     
    if path == None:                                                                                              
      left_prefix = '0'
      right_prefix = '1' 
    else:
      left_prefix = path + '0'
      right_prefix = path + '1' 
    # Create new left and right nodes, and remove original bucket
    parent_node.left = TreeNode(left_prefix)
    parent_node.right = TreeNode(right_prefix) 
    parent_node.delete_bucket() 
    new_closest_bucket, new_sister_bucket = self.new_buckets(closest_prefix_bit, parent_node) 
    
    # Keep track of peers that have been added to new buckets. 
    # If closest_k_bucket is STILL full, just returns without placing the last peer 
    for peer in peers:
      if peer.node_id[bit_matching_index] == closest_prefix_bit:
        new_closest_bucket.add_peer(peer)   
      else:  
        new_sister_bucket.add_peer(peer) 
    self.depth += 1 
    return

  def search(self, peer_id: int) -> PeerNode:
    tree_node, path = self.traverse(peer_id) 
    peer_node = tree_node.bucket.search(peer_id)                       
    if peer_node != None:
      return peer_node    
    return  

 
  # ----------------
  # Helper functions
  # ----------------
  
  #  Make 'path' an output of traverse.  Useful for differentiating between root node and intermediary node when splitting closest_k_bucket() 
  def traverse(self, peer: PeerNode) -> list[TreeNode, str]:
    path = ''
    root = self.root 
    distance = self.xor_distance(self.source_id, peer)

    if root.left == None and root.right == None:  
      return root, None
    if distance[0] == '1': 
      if self.source_id[0] == '0':
        return root.right, '1' 
      return root.left, '0'

    # Find path 
    for i in range(self.depth):
      if distance[i] == '0': 
        path = path + self.source_id[i] 
      # Provides an off ramp for peers that should be placed in intermediate buckets.
      else:
        path = path + peer[i] 
        break
    
    # Walk path to node
    for bit in path:
      if bit == '0':
        root = root.left 
      if bit == '1':
        root = root.right 
    return root, path 
  
  def xor_distance(self, s1: str, s2: str) -> str:
    xor_list = [str(ord(a) ^ ord(b)) for a,b in zip(s1,s2)]
    xor_diff = ''.join(xor_list)
    return xor_diff
  
  def new_buckets(self, bit: str, parent_node: TreeNode) -> list[TreeNode]:
    if bit == '0':
      return parent_node.left.bucket, parent_node.right.bucket 
    return parent_node.right.bucket, parent_node.left.bucket

  # ===========================
  # Routing Table Visualization 
  # ===========================
  def bredth_first_search(self, root: TreeNode) -> None:
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

      # Prints bucket(s) node_ids for each layer of the tree 
      for i in range(len(queue)):
        if queue[i].bucket != None:
          ids = [] 
          bucket = queue[i].bucket 
          for j in range(len(bucket.peers)):
            if bucket.peers[j] != -1:  
              ids.append(bucket.peers[j].node_id) 
            else:
              ids.append(-1) 
          queue_buckets.append((queue[i].prefix, ids)) 
          # queue_buckets.append((queue[i].prefix, queue[i].bucket.peers)) 
        if queue[i].left != None: 
          children.append(queue[i].left) 
        if queue[i].right != None:
          children.append(queue[i].right) 

      # Print second closest nodes, then closest nodes.  Separate the two buckets 
      if len(queue_buckets) > 0: 
        print(queue_buckets)
      
      queue = children
    return



#                   \\\\\\\\\\\\\\\///////////////
#                    ============================
#                         Create Hash Table
#                    ============================
#                   ///////////////\\\\\\\\\\\\\\\