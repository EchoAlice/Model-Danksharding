# =============
# ROUTING TABLE
# =============
def max_key(digits) -> int:
  n = int(digits) 
  return 2**n -1

k = 3
BIN_DIGITS = '16'
MAX_KEY = max_key(BIN_DIGITS)

# Delete this nonsense when I move REAL routing table into here
BIN_MAX_KEY = format(MAX_KEY, '0'+BIN_DIGITS+'b')
routing_table = [[-1]*k for i in range(len(BIN_MAX_KEY))]    




# ===========
# HASH TABLE 
# ===========


# ====
# BLOB
# ====
number_of_samples = 16
half_of_samples = int(number_of_samples/2)
original_data = []
extended_data = []

#   original data          extended data
# [0,1,2,3,4,5,6,7]  [8,9,10,11,12,13,14,15] 
# [T,T,T,T,T,T,T,T,    F,F,F,F,F,F,F,F,F]       proof at index.  Bool rn...  Make KZG Proof!
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


# ==========
# DATA TYPES
# ==========

# NodeID - 160 bit int
# Key -    160 bit int (typically hash of a string key)
# Value -   Byte array (fits in udp packet?)
# Nonce -  160 bit int.  Not sure what this is for