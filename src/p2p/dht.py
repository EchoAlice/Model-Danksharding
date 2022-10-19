import copy
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
  def __init__(self, node_id):  
    self.node_id = node_id               
    self.ip_address = None 
    self.udp_port = None 

# Keeps track of positions within the tree.
class TreeNode:
  def __init__(self, prefix):
    self.prefix = prefix 
    self.left = None
    self.right = None
    self.bucket = Bucket(prefix) 
  
  def delete_bucket(self):
    self.bucket = None 
    return

# The common prefix is its position in the tree.  Later: Add linked list functionality 
#
class Bucket:
  def __init__(self, prefix):  
    self.prefix = prefix
    self.peers = [-1]*k

  def add_peer(self, peer):
    first_empty_index = None 
    
    for i in range(len(self.peers)):
      # Finding first place to put peer 
      if self.peers[i] == -1: 
        if first_empty_index == None:
          first_empty_index = i
      # Making sure the peer isn't already inside of the bucket 
      else:
        if self.peers[i].node_id == peer.node_id:
          return
    
    if first_empty_index == None:
      return 'Full'
    self.peers[first_empty_index] = peer  
    return

  def delete_peer(self, peer):
    for i in range(len(self.peers)): 
      if self.peers[i] != -1: 
        if self.peers[i].node_id == peer.node_id: 
          self.peers[i] = -1
          return 
    print('Peer is not here') 
    return

  def search_bucket(self, peer) -> PeerNode:
    for i in range(len(self.peers)):
      if self.peers[i] == -1:
        pass
      else:
        if self.peers[i].node_id == peer:
          return self.peers[i] 
    return None


# =============
# Routing Table
# =============
#
class RoutingTable:
  def __init__(self, source_id): 
    self.source_id = source_id 
    self.root = TreeNode(None)                  
    self.depth = 0       # Prefix bits <= depth 

  def add_peer(self, peer: PeerNode) -> None:
    path = self.find_path(peer.node_id)                                     
    tree_node = self.traverse(self.root, path)
    add_peer_result = tree_node.bucket.add_peer(peer)
    
    # If full, check to see if it's at the closest bucket 
    if add_peer_result == 'Full':
      # if tree_node.left == None and tree_node.right == None or ____________________: 
      if path == None or tree_node.prefix[:self.depth] == self.source_id[:self.depth]:         
        peers = copy.deepcopy(tree_node.bucket.peers) 
        peers.append(peer)
        self.split_closest_k_bucket(path, tree_node, peers)            

    self.bredth_first_search(self.root)
    return

  # Only focus on removing peer for now.  Don't worry about deleting a bucket completely
  def delete_peer(self, peer):
    path = self.find_path(peer)
    tree_node = self.traverse(self.root, path)
    tree_node.bucket.delete_peer(peer) 
    return

  # If the k-bucket's range includes u's own node ID, then the bucket is split into two new 
  # buckets, the old contents divided between the two, and the insertion attempt repeated  
  def split_closest_k_bucket(self, path, parent_node, peers) -> None:
    bit_matching_index = self.depth 
    closest_prefix_bit = self.source_id[bit_matching_index]
     
    # CREATE NEW BUCKETS
    # if parent_node.left == None and parent_node.right == None: 
    if path == None:
      left_prefix = '0'
      right_prefix = '1' 
    else:
      # Parent_node.prefix 
      left_prefix = path + '0'
      right_prefix = path + '1' 

    # Create new left and right nodes, and remove original bucket
    parent_node.left = TreeNode(left_prefix)
    parent_node.right = TreeNode(right_prefix) 
    parent_node.delete_bucket() 

    # MOVE PEERS TO NEW BUCKETS
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

  # Visualizing the Routing Table 
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


  def search(self, peer_id: int) -> PeerNode:
    path = self.find_path(peer_id)
    tree_node = self.traverse(self.root, path) 
    peer_node = tree_node.bucket.search_bucket(peer_id) 
    print('Peer Node: '+str(peer_node)) 
    if peer_node != None:
      return peer_node    
    return  





  # Follow the path from root down to the correct node 
  def traverse(self, root, path) -> TreeNode:
    # At root node. No buckets have split
    if path == None:
      return root
    
    print('Path for node to be added: '+str(path))
    
    for bit in path:
      if bit == '0':
        root = root.left 
      if bit == '1':
        root = root.right 
    return root 


  # ----------------
  # Helper functions
  # ----------------

  # Finds correct path to tree node in order to place peer inside of its bucket 
  # Should find_path() be placed inside of traverse()? Do i ever use one without the other? 
  def find_path(self, peer) -> str:
    prefix = []
    distance = self.xor_distance(peer, self.source_id)
    
    if self.root.left == None and self.root.right == None: 
      return None
    if distance[0] == '1': 
      if self.source_id[0] == '0':
        return '1' 
      return '0'

    # This loop should only be cycled through as long as it hasn't surpassed the maximum depth 
    for i in range(self.depth):
      if distance[i] == '0': 
        prefix.append(self.source_id[i])
      # Provides an off ramp for peers that should be placed in intermediate buckets.
      else:
        prefix.append(peer[i]) 
        break
    return ''.join(prefix)

  def xor_distance(self, s1, s2) -> str:
    xor_list = [str(ord(a) ^ ord(b)) for a,b in zip(s1,s2)]
    xor_diff = ''.join(xor_list)
    return xor_diff
  
  def new_buckets(self, bit, parent_node) -> list[TreeNode]:
    if bit == '0':
      return parent_node.left.bucket, parent_node.right.bucket 
    return parent_node.right.bucket, parent_node.left.bucket




#                   \\\\\\\\\\\\\\\///////////////
#                    ============================
#                         Create Hash Table
#                    ============================
#                   ///////////////\\\\\\\\\\\\\\\