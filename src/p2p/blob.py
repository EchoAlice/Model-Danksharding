from config import ( extended_data,
                     half_of_samples,
                     number_of_samples,
                     original_data,
)

#  =============
#  Create a blob
#  =============
#      - Create a blob data type that mimics the real thing.  (original data, extended data, proof)
#      - Stub samples with fake data, then integrate these samples within node(s) hash table(s).  
#      - Once (most) functionality of DHT is created, make a lagrange algorithm that erasure codes
#        data within the blob.  
#
#                     I know there are implementations of lagrange algs out there,
#                     but i want to implement my own, so i can understand at a fundamental
#                     level what's going on.  I hope to one day be the guy writing these 
#                     algs that provide value to the ecosystem.
#
class Sample:
  def __init__(self, data, proof):
    self.data = int(data)
    self.proof = bool(proof)

class Blob:
  def __init__(self, samples): 
    self.samples = samples 



# ------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------
for i in range(number_of_samples):
  if i<half_of_samples:
    original_data.append(Sample(i, True))
  else:
    extended_data.append(Sample(i, False))

samples = original_data + extended_data