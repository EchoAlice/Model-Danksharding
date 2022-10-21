# =============
# ROUTING TABLE
# =============

# I should base this off of binary, not calculation
def max_key(digits) -> int:
  n = int(digits) 
  return 2**n -1

k = 3
MAX_BIN_DIGITS = '6'
MAX_KEY = max_key(MAX_BIN_DIGITS)



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
