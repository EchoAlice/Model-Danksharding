from helper import ( random_chunks_and_xs,
                     reed_solomon_data,
)
from remerkleable.basic import uint64, byte
from remerkleable.complex import Container, Vector

"""
  This file is trash right now...
  
  I need to instantiate a lagrange function that works much better
  in order to create a real blob.  And this seperate file for the
  blob isn't necessary.  Just encorperate lagrange logic in main.py
"""




#   Custom types 
Bytes16 = Vector[byte, 16]                        # Test value for now
Bytes512 = Vector[byte, 512]
sample = byte                                     # A sample is actually a 512 byte chunk!

#  =============
#  Create a blob
#  =============
#  - Use lagrange that works now to construct simplified version of blob
#  - Figure out how to create a mock DHT.
#    Why is my lagrange interpolation function nondeterministic???  
#  - Once lagrange is efficient, make blob size of 512 bytes

  
# Make blob input bytes16
string = 'ffffffffffffffff'
# file_chunks = string.encode('ascii')
original_data_test = [c for c in string.encode('ascii')] 

class Blob(Container): 
  original_data: Bytes16                           
  extended_data: Bytes16 
  # proof: list[KZG committment] 

# Input needs to be a list of bytes!
def create_blob(input) -> Blob:
  original_xs = list(range(1,len(input)+1))           
  extended_xs = list(range(len(input)+1, 2*len(input)+1))
  return Blob(
    original_data = input, 
    extended_data = reed_solomon_data(input, original_xs, extended_xs)
  )


# original_data = [1,3,2,1]
# original_xs = [1,2,3,4]
# extended_xs = [5,6,7,8]
original_data_test = [c for c in string.encode('ascii')] 
original_xs = list(range(1,len(original_data_test)+1))           
extended_xs = list(range(len(original_data_test)+1, 2*len(original_data_test)+1))

# print(reed_solomon_data(original_data_test, original_xs, extended_xs))



# RECONSTRUCT ORIGINAL DATA FROM BLOB DATA!
#-------------------------------------------
my_blob = create_blob(original_data_test)
all_chunks = my_blob.original_data+my_blob.extended_data
all_xs = original_xs+extended_xs
all_points = list(zip(all_xs, all_chunks))
points_chosen = random_chunks_and_xs(all_points)

data_chosen = []
correlated_xs = []
for i in range(len(points_chosen)):
  data_chosen.append(points_chosen[i][1])
  correlated_xs.append(points_chosen[i][0])

original_data_derived = Bytes16(reed_solomon_data(data_chosen, correlated_xs, original_xs))    



