# ==================
# BLOB CONFIGURATION
# ==================

number_of_samples = 16
half_of_samples = int(number_of_samples/2)
original_data = []
extended_data = []


#     original             extended
# [0,1,2,3,4,5,6,7]  [8,9,10,11,12,13,14,15] 
# [T,T,T,T,T,T,T,T,    T,T,T,T,T,T,T,T,T]       proof at index.  Bool rn...  Make KZG Proof!
class Sample:
  def __init__(self, data, proof):
    self.data = int(data)
    self.proof = bool(proof)

for i in range(number_of_samples):
  if i<half_of_samples:
    original_data.append(Sample(i, True))
  else:
    extended_data.append(Sample(i, False))

samples = original_data + extended_data