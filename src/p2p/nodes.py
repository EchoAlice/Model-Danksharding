from config import ( samples,
)
from routing_table import RoutingTable

'''
  Now that I'm mocking DAS blob interaction,  nodes should be requesting 
  individual samples (and proofs) from the proposer, and telling others within
  the network if they've validated their share, instead of storing data themselves.

  Think about what's needed from each node for a mock DHT
'''

class Blob:
  def __init__(self, samples): 
    self.samples = samples 

class VerifierNode:
  def __init__(self, id, samples):
    self.id = id                           
    self.samples = samples 
    self.routing_table = [int]                # List of neighbors the VerifierNode is responsible for (node_id)   


# This is our blob. Hi, Mr. Blob
mr_blob = Blob(samples)


# Create a routing table:
#
#    1. Which node is responsible for which samples?
#    2. Which neighbors should a node have?












# Verifier Node functions.  Can reinstantiate once routing table is implemented

'''
  def verify_sample(self, index) -> bool:
    if index not in self.sample_indexes[:self.num_samples]:
      return -1
    sample = self.request_for_sample(index)       
    availability = self.compute_proof(sample) 
    return availability 

  # Redundant because all data is on our local CPU, but mocks a real deal node 
  def request_for_sample(self, index):
    sample = blob.data[index]
    return sample

  def compute_proof(self, sample) -> bool:
    result = sample.proof 
    return result

  def request_neighbor(self, index):
    # Make sure neighbor you request is in your routing table  
    pass
'''

